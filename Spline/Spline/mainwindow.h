#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>
#include <QGraphicsScene>
#include <QGraphicsView>
#include <QSlider>
#include <QBoxLayout>
#include <QLabel>
#include <QCheckBox>

#include "spline.h"


namespace Ui {
    class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

public slots:
    void setValue(int i);

protected:
    void mousePressEvent(QMouseEvent *event);

private:
    void createScene();
    void createLayout();

private:
    size_t width;
    size_t height;

    Ui::MainWindow *ui;

    QGraphicsScene *scene;
    QGraphicsView *graphicsView;

    QSlider *slider;
    QLabel *label;
    QCheckBox *checkBoxSplineLine;
    QCheckBox *checkBoxSupportLines;

    Spline* spline;
};

#endif // MAINWINDOW_H
