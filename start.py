import threading
import subprocess

def app1():
    subprocess.run(['python', 'emotiv_server.py'])

def app2():
    subprocess.run(['python', 'memesocket.py'])

def app3():
    subprocess.run(['python', 'audio_stream.py'])

def app4():
    subprocess.run(['python', 'read_data.py'])

thread1 = threading.Thread(target=app1)
thread2 = threading.Thread(target=app2)
thread3 = threading.Thread(target=app3)
thread4 = threading.Thread(target=app4)

thread1.start()
thread2.start()
thread3.start()
thread4.start()

thread1.join()
thread2.join()
thread3.join()
thread4.join()