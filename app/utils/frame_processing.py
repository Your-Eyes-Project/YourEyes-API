import numpy as np
import cv2 as cv

def decode_frame(video_frame):
    try:
        y_width, y_height = video_frame.y_width, video_frame.y_height
        uv_width, uv_height = y_width, y_height // 2

        Y = np.frombuffer(video_frame.y_plane, dtype=np.uint8).reshape((y_height, y_width))

        u_data = np.frombuffer(video_frame.u_plane, dtype=np.uint8)
        u_data_padded = np.pad(u_data, (0, 1), 'constant', constant_values=0)
        U = u_data_padded.reshape((uv_height, uv_width))

        v_data = np.frombuffer(video_frame.v_plane, dtype=np.uint8)
        v_data_padded = np.pad(v_data, (0, 1), 'constant', constant_values=0)
        V = v_data_padded.reshape((uv_height, uv_width))

        U = cv.resize(U, (y_width, y_height), interpolation=cv.INTER_LINEAR)
        V = cv.resize(V, (y_width, y_height), interpolation=cv.INTER_LINEAR)

        YUV = cv.merge([Y, U, V])

        rgb = cv.cvtColor(YUV, cv.COLOR_YUV2BGR)
        rgb = cv.rotate(rgb, cv.ROTATE_90_CLOCKWISE)

        return rgb
    except Exception as e:
        print(f"Error decoding frame: {e}")
        return None
