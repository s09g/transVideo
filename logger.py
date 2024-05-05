import logging

def setup_logging(video_id):
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename=f'video/{video_id}/app.log',
                        filemode='w')