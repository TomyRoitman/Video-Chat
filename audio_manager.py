import threading
import time

import sounddevice as sd
from scipy.io.wavfile import write


class Audio():

    def __init__(self, seconds, muted=False, FPS=24):
        self.fs = 44100  # Sample rate
        self.seconds = seconds
        self.current_playing = None
        self.participant_tracks_in_queue = []
        self.running = True
        self.muted = muted
        self.user_tracks_in_queue = []
        self.lock = threading.Lock()
        self.total_tracks = 0
        self.state = 0

    def sound_recorder(self, record_only=True):
        recording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, channels=1)
        sd.wait()
        self.lock.acquire()
        self.user_tracks_in_queue.append(recording)
        self.lock.release()
        while self.running:
            if not self.muted:
                if self.participant_tracks_in_queue:
                    # print(time.time(), 'playing')
                    current_playing = self.participant_tracks_in_queue.pop(0)
                    self.state = 1
                    recording = sd.playrec(current_playing, samplerate=self.fs, channels=1)
                    sd.wait()
                    # print(time.time(), 'finished playing')

                elif self.total_tracks == 0 or record_only:
                    # print(time.time(), 'recording')
                    self.state = 2
                    recording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, channels=1)
                    sd.wait()
                    # print(time.time(), 'finished recording')

                self.lock.acquire()
                self.user_tracks_in_queue.append(recording)
                self.lock.release()
            else:
                self.user_tracks_in_queue = []

    def export_sound(self):
        if not self.muted and self.user_tracks_in_queue:
            # self.lock.acquire()
            recording = self.user_tracks_in_queue.pop(0)
            # self.lock.release()
            return recording
        else:
            return None

    def add_track(self, track):
        if self.__is_valid_track(track):
            self.lock.acquire()
            self.participant_tracks_in_queue.append(track)
            self.total_tracks += 1
            self.lock.release()

    def __is_valid_track(self, track):
        return True

    def play_sound(self):
        seconds = self.seconds
        starting_time = time.time()
        while self.running:
            if time.time() - starting_time >= self.seconds:
                if self.participant_tracks_in_queue:
                    current_playing = self.participant_tracks_in_queue.pop(0)
                    print('playing sound')
                    sd.play(current_playing)
                    # sd.wait()
                    # thread = AudioThread(current_playing)
                    # thread.set_duration(int(self.seconds * self.fs))
                    # thread.start()
                    # time.sleep(self.seconds)
                    # thread.stop()
                starting_time = time.time()


# seconds = 3  # Duration of recording
# print('recording')
# sd.wait()  # Wait until recording is finished
# print('finished recording')
# print('\n\nplaying')
# sd.play(myrecording)
# print('done playing')
# sd.wait()
# write('output.wav', fs, myrecording)  # Save as WAV file

class AudioThread(threading.Thread):
    def __init__(self, track):
        threading.Thread.__init__(self)
        self.track = track

    def set_duration(self, duration):
        self.duration = duration

    def run(self):
        sd.play(self.track, self.duration, blocking=True)

    def stop(self):
        sd.stop()
