#include "mainwindow.h"
#include "ui_mainwindow.h"

#include "point.h"
#include "label.h"

#include <QDebug>
#include <QMouseEvent>


MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow)
{
    ui->setupUi(this);

    width = 1024;
    height = 720;

    setWindowTitle("Spline");
    setFixedSize((int)width, (int)height);

    createScene();
    createLayout();

    spline = new Spline(scene);

    connect(slider, SIGNAL(valueChanged(int)), spline, SLOT(setParam(int)));

    connect(checkBoxSplineLine, SIGNAL(stateChanged(int)), spline, SLOT(setSplineLineStatus(int)));
    connect(checkBoxSupportLines, SIGNAL(stateChanged(int)), spline, SLOT(setSupportLinesStaus(int)));
}

MainWindow::~MainWindow()
{
    delete ui;

    delete slider;
    delete label;
    delete checkBoxSplineLine;
    delete checkBoxSupportLines;

    delete scene;
    delete graphicsView;

    delete spline;
}

void MainWindow::setValue(int i)
{
    qDebug() << "new slider value: " << i << "\n";
}

void MainWindow::createScene()
{
    scene = new QGraphicsScene();

    graphicsView = new QGraphicsView(scene, this);
    graphicsView->setRenderHint(QPainter::Antialiasing);
    graphicsView->setSceneRect(50, 50, 350, 350);
    graphicsView->setFixedSize((int)width, (int)height);
}

void MainWindow::createLayout()
{
    slider = new QSlider(Qt::Horizontal, graphicsView);
    slider->setFixedWidth(200);
    slider->setValue(Spline::defaultParamValue());
    slider->setMaximum(100);

    label = new ParamLabel(graphicsView);
    label->setFixedSize(50, 20);
    label->move(200, 0);

    checkBoxSplineLine = new QCheckBox("Show spline line", graphicsView);
    checkBoxSplineLine->setFixedSize(100, 20);
    checkBoxSplineLine->move(0, 20);
    checkBoxSplineLine->setChecked(true);

    checkBoxSupportLines = new QCheckBox("Show support lines", graphicsView);
    checkBoxSupportLines->setFixedSize(100, 20);
    checkBoxSupportLines->move(0, 40);
    checkBoxSupportLines->setChecked(true);

    connect(slider, SIGNAL(valueChanged(int)), label, SLOT(setNum(int)));
}

void MainWindow::mousePressEvent(QMouseEvent *event)
{
    QPointF pos = graphicsView->mapToScene(event->pos());
    Point *point = new SupportPoint(pos, scene, spline);

    scene->addItem(point);
    spline->addPoint(point);

    connect(point, SIGNAL(pointMoved()), spline, SLOT(redraw()));

    spline->draw();
}
