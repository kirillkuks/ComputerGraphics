#ifndef SPLINE_H
#define SPLINE_H

#include "point.h"

#include <QList>
#include <QWidget>
#include <QPen>


class Point;
class Spline;


class Spline : public QObject
{
    Q_OBJECT

public:
    static int defaultParamValue();

public:
    explicit Spline(QGraphicsScene *scene);
    virtual ~Spline();

    void addPoint(Point *point);
    void removePoint(Point *point);

    void draw();

    void buildSplineLine();

public slots:
    void setParam(int param);
    void redraw();

    void setSplineLineStatus(int state);
    void setSupportLinesStaus(int state);

signals:
    void paramChanged();

private:
    void drawDeCasteljau(QList<QPointF> const& supportPoints);

    void drawLines(QList<QPointF> const& points, QList<QGraphicsItem*>& targetBuffer, QPen const& pen = QPen(QBrush(Qt::black), 1));

    QList<QPointF> firstSupportPoints();
    QList<QPointF> calculateNextSupportPoints(QList<QPointF> const& supportPoints);

    QPointF calculateSplinePoint(double param);

    void deleteLines(QList<QGraphicsItem*>& buffer);
    void deleteSplinePoint();

private:
    static int const defaultParam = 50;

private:
    QList<Point*> points;
    QList<QGraphicsItem*> lines;
    QList<QGraphicsItem*> splineLines;

    QGraphicsScene *targetScene;

    Point* splinePoint;

    double t;
    bool needDrawLine;

    bool drawSplineLine;
    bool drawSupportLines;

};

#endif // SPLINE_H
