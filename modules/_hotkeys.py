from pynput import keyboard

hotkeys = [
    (['0', keyboard.Key.ctrl], window.comboBox_rating.setCurrentIndex(0)),
    (['1', keyboard.Key.ctrl], window.comboBox_rating.setCurrentIndex(1)),
    (['2', keyboard.Key.ctrl], window.comboBox_rating.setCurrentIndex(2)),
    (['3', keyboard.Key.ctrl], window.comboBox_rating.setCurrentIndex(3)),
    (['4', keyboard.Key.ctrl], window.comboBox_rating.setCurrentIndex(4)),
    (['5', keyboard.Key.ctrl], window.comboBox_rating.setCurrentIndex(5)),
]
