#ifndef POINT_H
#define POINT_H

#include <QGraphicsEllipseItem>
#include <QObject>

#include "spline.h"


class Spline;


class Point : public QObject, public QGraphicsEllipseItem
{
    Q_OBJECT

public:
    explicit Point(QRectF const& pt, QGraphicsScene *scene, Spline *spline);
    ~Point();

    QPointF center() const;

    QGraphicsScene *parentScene;
    Spline *parentSpline;
    QPointF cent;
};


class SupportPoint : public Point
{
    Q_OBJECT

public:
    explicit SupportPoint(QPointF const& pt, QGraphicsScene *scene, Spline *spline);
    ~SupportPoint();

signals:
    void pointMoved();

protected:
    void mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event);
    void mouseMoveEvent(QGraphicsSceneMouseEvent *event);

private:
    static double const rad = 10.0;
};


class SplinePoint : public Point
{
public:
    explicit SplinePoint(QPointF const& pt, QGraphicsScene *scene, Spline *spline);
    ~SplinePoint();

private:
    static double const rad = 7.0;

private:

};


#endif // POINT_H
