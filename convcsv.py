import pyrealsense2 as rs
import numpy as np
import pandas as pd

def process_frame(frame):
    """
    Process an individual frame and return a dictionary of extracted data.
    For video frames (depth, infrared, color), compute summary statistics.
    For motion frames (gyro, accelerometer), record x, y, z values.
    """
  
    stream_type = frame.get_profile().stream_type()
    timestamp = frame.get_timestamp()
    
    # Create a record dictionary with common fields  
    record = {"timestamp": timestamp, "stream": str(stream_type)}
    
    # Process video frames
    if stream_type in [rs.stream.depth, rs.stream.infrared, rs.stream.color]:
        data = np.asanyarray(frame.get_data())
        record["avg_value"] = np.mean(data)
        record["std_value"] = np.std(data)
        record["min_value"] = np.min(data)
        record["max_value"] = np.max(data)
    
    # Process motion frames (gyroscope or accelerometer)
    elif stream_type in [rs.stream.gyro, rs.stream.accel]:
        motion_frame = frame.as_motion_frame()
        motion_data = motion_frame.get_motion_data()  # returns a structure with x, y, z attributes
        record["x"] = motion_data.x
        record["y"] = motion_data.y
        record["z"] = motion_data.z

    # For any other stream types, you might add additional processing here
    
    return record

def main():
    
    bag_file = input("Enter the path to the RealSense .bag file: ")
    csv_file = input("Enter the output CSV file name (default: output.csv): ") or "output.csv"

    # Create a pipeline and configure it to read from the bag file.
    pipeline = rs.pipeline()
    config = rs.config()
    # Enable playback from the given file and disable looping playback.
    config.enable_device_from_file(bag_file, repeat_playback=False)
    
    # Start the pipeline
    try:
        pipeline_profile = pipeline.start(config)
    except Exception as e:
        print("Could not start pipeline. Please check the bag file path and content.")
        print(e)
        return

    frames_data = []
    print("Processing frames from the bag file...")
    
    try:
        # Loop until no more frames are available.
        while True:
            # wait_for_frames() will block until the next set of frames is available
            frames = pipeline.wait_for_frames(timeout_ms=1000)
            if not frames:
                # No frames available: end of file reached.
                break
            
            # A frameset may contain several frames (one for each enabled stream)
            for frame in frames:
                try:
                    record = process_frame(frame)
                    frames_data.append(record)
                except Exception as proc_e:
                    print("Error processing a frame:", proc_e)
                    continue
    except Exception as e:
        # When the bag file ends, an exception may be thrown. You can catch and ignore it.
        print("Finished processing or encountered an error:", e)
    finally:
        pipeline.stop()
    
    # Create a pandas DataFrame from the collected frame data.
    df = pd.DataFrame(frames_data)
    df.to_csv(csv_file, index=False)
    print(f"Data has been exported to {csv_file}")

if __name__ == "__main__":
    main()
