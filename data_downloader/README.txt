to download json of all the current queuery snapshot, use:

ruby json_downloader.rb --path="/home/tommy/myenv/workspace/data/onepunch/"

to download the pb file for the order information, use python download_pb.py .
the file will be first downloaded to s3://files.development.hover.to/tommy_tat_data/

aws s3 sync s3://files.development.hover.to/tommy_tat_data/ .