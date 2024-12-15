import glob

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMainWindow, QLabel, QScrollArea, QApplication
from XGmodel import model
import os

output_dir = "C:\\Users\MAZEN\PycharmProjects\XG_MODEL\plots"

class Menu(QWidget):
    def __init__(self):
        super().__init__()
        self.button_list = ButtonList('')
        self.setWindowTitle("Menu")
        self.setGeometry(700, 300, 500, 500)

        layout = QVBoxLayout()

        # Add stretch at the top to center the buttons vertically
        layout.addStretch(1)

        # Create four buttons
        self.button1 = QPushButton("Linear Regression", self)
        self.button2 = QPushButton("Logistic Regression", self)
        self.button3 = QPushButton("Advanced Logistic Regression", self)
        self.button4 = QPushButton("Exit", self)

        layout.setSpacing(20)
        # Connect button actions
        self.button1.clicked.connect(self.handle_button_click)
        self.button2.clicked.connect(self.handle_button_click)
        self.button3.clicked.connect(self.handle_button_click)
        self.button4.clicked.connect(self.exit)  # Exit button to close the application

        # Add buttons to the layout
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)
        layout.addWidget(self.button3)
        layout.addWidget(self.button4)

        # Add stretch at the bottom to center the buttons vertically
        layout.addStretch(1)

        # Set the layout for the Menu
        self.setLayout(layout)

    def handle_button_click(self):
        button = self.sender()
        if button:
            chosen_text = button.text()
            self.button_list.set_algo(chosen_text)
            self.close()
            self.button_list.show()

    def exit(self):
        QApplication.quit()

    def set_window2(self, window2):
        self.window2 = window2

    def set_plot(self, plot):
        self.plot = plot

    def set_button_list(self, button_list):
        self.button_list = button_list


class PlotWindow(QMainWindow):
    def __init__(self, images, team_data):
        super().__init__()
        self.setWindowTitle("Plots in PyQt5")
        self.setGeometry(700, 300, 500, 500)

        # List of images to display (from the argument passed)
        self.images = images
        self.team_data = team_data  # Store the team data

        # Create the central widget and scroll area
        scroll_area = QScrollArea()
        central_widget = QWidget()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(central_widget)
        self.setCentralWidget(scroll_area)

        # Create a layout to hold the image labels and the team data
        layout = QVBoxLayout()

        # Display the team data
        for team in self.team_data:
            team_label = QLabel(f"Team: {team['team']}\n"
                                f"Actual Goals: {team['actual_goals']}\n"
                                f"Our XG: {team['our_xg']}\n"
                                f"StatsBomb XG: {team['statsbomb_xg']}\n")
            team_label.setStyleSheet("font-size: 14px; font-weight: bold; margin-bottom: 10px;")
            layout.addWidget(team_label)

        # Add a separator line before the images (optional)
        separator = QLabel("-" * 40)
        separator.setAlignment(Qt.AlignCenter)
        layout.addWidget(separator)

        # Loop through the images list and create a label for each image
        self.labels = []  # List to keep track of all QLabel instances
        for image_path in self.images:
            label = QLabel(self)
            label.setScaledContents(True)  # Make sure the image is scaled to fit
            pixmap = QPixmap(image_path)  # Load the image from file path

            # Scale the pixmap to fit within a smaller size
            scaled_pixmap = pixmap.scaled(400, 300, Qt.KeepAspectRatio, Qt.SmoothTransformation)
            label.setPixmap(scaled_pixmap)  # Set the scaled image on the label

            layout.addWidget(label)  # Add the label to the layout
            self.labels.append(label)

        # Set the layout to the central widget
        central_widget.setLayout(layout)

    def set_team_data(self, team_data):
        self.team_data = team_data


class ButtonList(QWidget):
    def __init__(self, algo):
        super().__init__()
        self.setWindowTitle("64 Buttons Example")
        self.setGeometry(700, 300, 400, 500)

        # Create a scroll area to handle many buttons
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Create a central widget to hold the buttons
        central_widget = QWidget()
        scroll_area.setWidget(central_widget)

        # Create a vertical layout to display the buttons
        vbox_layout = QVBoxLayout()

        new_list = []
        for index, match in model.df_match.iterrows():  # Use iterrows() to loop over DataFrame rows
            new_entry = {
                'match_id': match['match_id'],
                'home_team_name': match['home_team_name'],
                'away_team_name': match['away_team_name']
            }
            new_list.append(new_entry)

        match_to_id = {}
        # Loop over the list and create buttons
        for item in new_list:
            s = f"{item['home_team_name']} Vs {item['away_team_name']}"
            match_to_id[s] = item['match_id']
            button = QPushButton(s, self)
            button.clicked.connect(self.handle_button_click)
            vbox_layout.addWidget(button)

        self.dict = match_to_id
        # Set the layout for the central widget
        central_widget.setLayout(vbox_layout)

        # Create a main layout and add the scroll area
        main_layout = QVBoxLayout()
        main_layout.addWidget(scroll_area)

        self.setLayout(main_layout)

    def handle_button_click(self):
        button = self.sender()
        team_data = [
            {'team': 'Argentina', 'actual_goals': 3, 'our_xg': 2.85, 'statsbomb_xg': 2.70},
            {'team': 'France', 'actual_goals': 2, 'our_xg': 2.10, 'statsbomb_xg': 2.05},
        ]

        if button:
            ret = []
            id = self.dict[button.text()]
            model.visualize_pitch(id)
            plot = os.path.join(output_dir, f"pitch_{id}.jpg")
            if self.algo == 'Logistic Regression':
                ret = model.evaluate_xg_logistic(id)
                model.visualize_shot_distance_vs_xg_logistic()
                model.visualize_shot_angle_vs_xg_logistic()
                img1 = os.path.join(output_dir, "angle_vs_xg_logistic.jpg")
                img2 = os.path.join(output_dir, "distance_vs_xg_logistic.jpg")
                self.plot = PlotWindow([img1, img2, plot], ret)
            elif self.algo == 'Advanced Logistic Regression':
                ret = model.evaluate_xg_adv(self.dict[button.text()])
                model.visualize_shot_distance_vs_xg_logistic()
                model.visualize_shot_angle_vs_xg_logistic()
                img1 = os.path.join(output_dir, "angle_vs_xg_logistic.jpg")
                img2 = os.path.join(output_dir, "distance_vs_xg_logistic.jpg")
                self.plot = PlotWindow([img1, img2, plot], ret)
            else:
                model.visualize_shot_angle_vs_xg_linear()
                img1 = os.path.join(output_dir, "angle_vs_xg_lin.jpg")
                img2 = os.path.join(output_dir, "distance_vs_xg_lin.jpg")
                self.plot = PlotWindow([img1, img2, plot], [])

            files = glob.glob(os.path.join(output_dir, "*"))
            for file in files:
                os.remove(file)  # Delete each file
            self.close()

            self.plot.show()

    def set_algo(self, algo):
        self.algo = algo

    def set_items(self, items):
        self.items = items

    def set_plot(self, plot):
        self.plot = plot


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Main Window")
        self.setGeometry(700, 300, 500, 500)

        # Create both windows
        self.menu = Menu()

        # Show the Menu window initially
        self.menu.show()
