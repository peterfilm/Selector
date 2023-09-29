def blocker(mw, value):
    if value == 0:
        mw.pushButton_cancel.show()
    else:
        mw.pushButton_cancel.hide()
        
    mw.pushButton_enter.setEnabled(value)
    mw.lineEdit_files.setEnabled(value)
    mw.pushButton_files.setEnabled(value)
    mw.pushButton_openFolder.setEnabled(value)
    mw.pushButton_find.setEnabled(value)
    mw.checkBox_dir.setEnabled(value)
    
    if mw.checkBox_dir.checkState():
        mw.lineEdit_path.setEnabled(value)
        mw.pushButton_path.setEnabled(value)
        mw.pushButton_copy.setEnabled(value)
        mw.pushButton_changeDir.setEnabled(value)