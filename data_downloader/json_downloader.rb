require 'json'
require 'fileutils'
require 'aws-sdk'
require 'parallel'
require 'connection_pool'

ARGS = Hash[ARGV.join(' ').scan(/--?([^=\s]+)(?:=(\S+))?/)]
if (ARGS["path"])
  puts "filepath is ->: " + ARGS["path"]
  Dir.chdir ARGS["path"]
  DOWNLOAD_FOLDER_PREFIX = "dashboard_data"
  Dir.mkdir(DOWNLOAD_FOLDER_PREFIX) unless Dir.exist?(DOWNLOAD_FOLDER_PREFIX)
end

CONNECTION_POOL = ConnectionPool.new(size: 30, timeout: 10) { Aws::S3::Client.new(region: "us-east-1") }

class DashboardOrderCountDownloader
  ORDER_STATS_PREFIX = "automation_data_dumps/dashboard_order_counts/"
  DOWNLOAD_FOLDER_PREFIX = "dashboard_data"
  Dir.mkdir(DOWNLOAD_FOLDER_PREFIX) unless Dir.exist?(DOWNLOAD_FOLDER_PREFIX)
    
  def initialize(**opts)
    @starting_id = opts[:starting_id].to_i

    @ids_to_download = ARGS["ids"].to_s.split(',').map(&:to_i)
    @ids_to_download = @ids_to_download.empty? ? [] : @ids_to_download
  end

  def download_batch(s3_object_batch)
    Parallel.each(s3_object_batch.to_a, in_threads: 25, progress: "Downloading dashboard order counts") do |s3_object|
      id = s3_object.key[/\d+/].to_i

      if (id >= @starting_id && @ids_to_download.empty?) || @ids_to_download.include?(id)
        filepath = "#{DOWNLOAD_FOLDER_PREFIX}/#{s3_object.key.split('/').last}"
        unless File.exists?(filepath)
          # `aws s3 cp s3://files.production.hover.to/#{s3_object.key} #{filepath}`
          #s3_object.download_file(filepath)
          CONNECTION_POOL.with do |s3|
            s3.get_object({ bucket: "files.production.hover.to", key: s3_object.key }, target: filepath)
          end
        end
      end
    end
  end

  def download_all
    batches = nil
    CONNECTION_POOL.with do |s3|
      objects = Aws::S3::Bucket.new("files.production.hover.to", client: s3).objects(prefix: ORDER_STATS_PREFIX)
      puts "Total objects: #{objects.count}"
      batches = objects.batches
    end
    total_batches = batches.count
    batches.each_with_index do |s3_object_batch, i|
      puts "Downloading Batch #{i + 1}/#{total_batches}"
      download_batch(s3_object_batch)
    end
  end

end

DashboardOrderCountDownloader.new.download_all
