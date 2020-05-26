import sounddevice as sd
from scipy.io.wavfile import write


class Audio():

    def __init__(self, muted=False, FPS=24):
        self.fs = 44100  # Sample rate
        self.seconds = 2
        self.current_playing = None
        self.participant_tracks_in_queue = []
        self.running = True
        self.muted = muted
        self.user_tracks_in_queue = []

    def sound_recorder(self):
        while self.running:
            if not self.muted:
                recording = sd.rec(int(self.seconds * self.fs), samplerate=self.fs, channels=2)
                sd.wait()
                self.user_tracks_in_queue.append(recording)
            else:
                self.user_tracks_in_queue = []

    def export_sound(self):
        if not self.muted and self.user_tracks_in_queue:
            recording = self.user_tracks_in_queue.pop(0)
            return recording
        else:
            return None

    def add_track(self, track):
        if self.__is_valid_track(track):
            self.participant_tracks_in_queue.append(track)

    def __is_valid_track(self, track):
        return True

    def play_sound(self):

        while self.running:

            if self.participant_tracks_in_queue:
                self.current_playing = self.participant_tracks_in_queue.pop(0)
                sd.play(self.current_playing)
                sd.wait()

# seconds = 3  # Duration of recording
# print('recording')
# sd.wait()  # Wait until recording is finished
# print('finished recording')
# print('\n\nplaying')
# sd.play(myrecording)
# print('done playing')
# sd.wait()
# write('output.wav', fs, myrecording)  # Save as WAV file
