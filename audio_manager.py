import threading
import time

import sounddevice as sd
from scipy.io.wavfile import write


class Audio():

    def __init__(self, muted=False, FPS=24):
        self.fs = 44100  # Sample rate
        self.seconds = 1
        self.current_playing = None
        self.participant_tracks_in_queue = []
        self.running = True
        self.muted = muted
        self.user_tracks_in_queue = []
        self.lock = threading.Lock()


    def sound_recorder(self):
        while self.running:
            if not self.muted:
                recording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, channels=1)
                sd.wait()
                self.lock.acquire()
                self.user_tracks_in_queue.append(recording)
                self.lock.release()
            else:
                self.user_tracks_in_queue = []

    def export_sound(self):
        if not self.muted and self.user_tracks_in_queue:
            self.lock.acquire()
            recording = self.user_tracks_in_queue.pop(0)
            self.lock.release()
            return recording
        else:
            return None

    def add_track(self, track):
        if self.__is_valid_track(track):
            self.lock.acquire()
            self.participant_tracks_in_queue.append(track)
            self.lock.release()

    def __is_valid_track(self, track):
        return True

    def play_sound(self):

        while self.running:
            if self.participant_tracks_in_queue:
                current_playing = self.participant_tracks_in_queue.pop(0)
                # sd.play(self.current_playing)
                # sd.wait()
                thread = AudioThread(current_playing)
                thread.start()
                time.sleep(self.seconds)
                thread.stop()

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

    def run(self):
        sd.play(self.track, blocking=True)

    def stop(self):
        sd.stop()
