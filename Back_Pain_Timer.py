import customtkinter as ctk
import pygame
from CTkMessagebox import CTkMessagebox
from tkinter import ttk


pygame.init()

should_start = True
take_a_break_counter = 0
notification_volume = 0.1

remaining_time = 15 * 60 + 1


def start_and_change_button_functions():
    global should_start
    should_start = True
    change_to_stop_button()
    update_timer()
    progress_bar.start(remaining_time * 10)


def change_to_stop_button():
    start_timer_button.pack_forget()
    stop_timer_button.pack()


def change_to_start_button():
    global should_start
    global remaining_time
    should_start = False
    remaining_time = 15 * 60 + 1
    time_left_label.configure(root, text="15 : 00")
    stop_timer_button.pack_forget()
    start_timer_button.pack()
    progress_bar.stop()


def message_notification(message: str):
    play_notification()
    CTkMessagebox(message=message, title="Time's Up")


def play_notification():
    pygame.mixer.music.load("Time is up notification sound.mp3")
    pygame.mixer.music.set_volume(notification_volume)
    pygame.mixer.music.play()


def update_timer():
    global take_a_break_counter
    global remaining_time
    if should_start:
        if remaining_time > 0:
            remaining_time -= 1
            minutes = remaining_time // 60
            seconds = remaining_time % 60
            time_left_label.configure(root, text=f"{minutes:02d} : {seconds:02d}")
            root.after(1000, update_timer)
        else:
            if take_a_break_counter == 0:
                message_notification("Please Change Your Sitting Position")
                take_a_break_counter += 1
                change_to_start_button()
            else:
                message_notification(
                    "Please Take A Break, Walk And Look At Objects That Are Far From You"
                )
                take_a_break_counter -= 1
                change_to_start_button()
    else:
        return


root = ctk.CTk()
root.geometry("400x200")
root.title("Back Pain Timer")

frame1 = ctk.CTkFrame(root, fg_color="transparent")


time_left_label = ctk.CTkLabel(frame1, text="15 : 00")
start_timer_button = ctk.CTkButton(
    frame1,
    text="Start Timer",
    command=start_and_change_button_functions,
    fg_color="#1AA6B7",
    hover_color="#348498",
)
stop_timer_button = ctk.CTkButton(
    frame1,
    text="Stop Timer",
    fg_color="#FF414D",
    hover_color="#F56A79",
    command=change_to_start_button,
)


progress_bar = ttk.Progressbar(root, mode="determinate", length=300)

frame1.pack(pady=50)
time_left_label.pack()
progress_bar.pack()
start_timer_button.pack()
root.mainloop()


# need to style the application with a progress bar,
# after that, need to add a way to increase or decrease the volume of the notification from within the UI.
