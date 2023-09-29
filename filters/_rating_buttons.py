from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, pyqtSignal, QEvent


class RatingWidget(QWidget):
    ratingChanged = pyqtSignal(int)  # Custom signal to indicate rating change

    def __init__(self):
        super().__init__()

        self.rating = 0  # Initial rating value
        self.enabled = 0 # disabled for default
        self.previous_rating = 0  # Previous rating value
        self.max_rating = 5  # Maximum rating value
        self.star_images = {
            "active": QPixmap("img/star.png"),
            "inactive": QPixmap("img/nostar.png"),
            "disabled": QPixmap("img/disabledstar.png"),  # Added disabled star image
        }

        layout = QHBoxLayout()
        self.star_labels = []

        # Create star labels and add them to the layout
        for i in range(self.max_rating):
            star_label = QLabel()
            star_label.mousePressEvent = lambda event, index=i: self.toggle_rating(index + 1)  # Toggle rating when clicked
            star_label.installEventFilter(self)  # Install event filter for hover effect
            layout.addWidget(star_label)
            self.star_labels.append(star_label)

        self.setLayout(layout)
        self.set_rating(self.rating)
        self.hovered_rating = 0  # Store the hovered rating
        
        self.setEnabled(self.enabled) # установки активности

    def set_rating(self, rating):
        if hasattr(self, 'enabled') and not self.enabled:
            return  # Do not allow changes if disabled
    
                
        if rating != self.rating:
            self.rating = rating
            for i, star_label in enumerate(self.star_labels):
                if i < rating:
                    star_label.setPixmap(self.star_images["active"])
                else:
                    star_label.setPixmap(self.star_images["inactive"])
            self.ratingChanged.emit(self.rating)  # Emit the custom signal

    def toggle_rating(self, rating):
        # выставление рейтинга
        if hasattr(self, 'enabled') and not self.enabled:
            return  # Do not allow changes if disabled from click

        if rating == self.rating:
            # Toggle rating: If clicking the selected rating again, set it to 0 and show all stars as "nostar"
            self.set_rating(0)
        else:
            self.set_rating(rating)
            
    def setEnabled(self, value):
        self.enabled = value
        if value == 1:
            for i, star_label in enumerate(self.star_labels):
                star_label.setPixmap(self.star_images["inactive"])
                star_label.setCursor(Qt.PointingHandCursor)
        elif value == 0:
            for i, star_label in enumerate(self.star_labels):
                star_label.setPixmap(self.star_images["disabled"])
                star_label.setCursor(Qt.ArrowCursor)

    def get_rating(self):
        return self.rating

    def eventFilter(self, source, event):
        # эвент
        if hasattr(self, 'enabled') and not self.enabled:
            return False  # Do not process events if disabled

        if event.type() == QEvent.Enter:
            # Hover effect when the mouse enters the star label
            index = self.star_labels.index(source)
            self.hover_star(index + 1)
        elif event.type() == QEvent.Leave:
            # Clear hover effect when the mouse leaves the star label
            self.clear_hover()

        return super().eventFilter(source, event)

    def clear_hover(self):
        # Clear the hover effect and restore the selected rating
        self.hovered_rating = 0
        self.hover_star(self.rating if self.rating > 0 else self.previous_rating)

    def hover_star(self, rating):
        # Show hover effect without changing the rating
        self.hovered_rating = rating
        for i, star_label in enumerate(self.star_labels):
            if i < rating:
                star_label.setPixmap(self.star_images["active"])
            else:
                star_label.setPixmap(self.star_images["inactive"])