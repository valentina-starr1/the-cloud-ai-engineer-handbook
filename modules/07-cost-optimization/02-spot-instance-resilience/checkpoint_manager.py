"""
Checkpoint manager: listens for termination signals and uploads model state to S3.
This is an illustrative example — adapt to your training stack (PyTorch, TensorFlow).
"""
import signal
import threading
import time
import boto3
import os

S3_BUCKET = os.environ.get('CHECKPOINT_BUCKET', 'my-checkpoints')
S3_PREFIX = os.environ.get('CHECKPOINT_PREFIX', 'model/')

s3 = boto3.client('s3')

checkpoint_lock = threading.Lock()
shutdown_requested = False

def save_checkpoint(local_path: str, key: str):
    # Upload and ensure atomicity with a temporary key and rename (copy+delete) pattern
    tmp_key = key + '.tmp'
    s3.upload_file(local_path, S3_BUCKET, tmp_key)
    s3.copy_object(Bucket=S3_BUCKET, CopySource={'Bucket': S3_BUCKET, 'Key': tmp_key}, Key=key)
    s3.delete_object(Bucket=S3_BUCKET, Key=tmp_key)

def perform_checkpoint():
    with checkpoint_lock:
        # Placeholder: replace with real model checkpoint save
        local_path = '/tmp/model.ckpt'
        with open(local_path, 'wb') as f:
            f.write(b'checkpoint')
        key = S3_PREFIX + 'checkpoint-' + str(int(time.time())) + '.ckpt'
        save_checkpoint(local_path, key)
        print('Checkpoint uploaded to s3://{}/{}'.format(S3_BUCKET, key))

def handle_termination(signum, frame):
    global shutdown_requested
    print('Termination signal received:', signum)
    shutdown_requested = True
    perform_checkpoint()
    # Exit after checkpointing
    os._exit(0)

def start_signal_handlers():
    signal.signal(signal.SIGTERM, handle_termination)
    signal.signal(signal.SIGINT, handle_termination)

if __name__ == '__main__':
    start_signal_handlers()
    print('Checkpoint manager running. PID:', os.getpid())
    # Simulate long-running job
    while True:
        time.sleep(5)
        if shutdown_requested:
            break
