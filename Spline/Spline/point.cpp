#include "point.h"

#include <QDebug>
#include <QApplication>
#include <QBrush>
#include <QGraphicsScene>
#include <QGraphicsSceneMouseEvent>


Point::Point(const QRectF &pt, QGraphicsScene *scene, Spline *spline) :
    QGraphicsEllipseItem(pt),
    parentScene(scene),
    parentSpline(spline)
{

}

Point::~Point()
{

}

QPointF Point::center() const
{
    return cent + pos();
}

///////////////////////////////////////////////////////////////////////////////////////////////////

SupportPoint::SupportPoint(QPointF const& pt, QGraphicsScene *scene, Spline *spline) :
    Point(QRectF(pt.x() - rad, pt.y() - rad, 2 * rad, 2 * rad), scene, spline)
{
    cent = pt;

    setBrush(QBrush(Qt::black));
    setFlag(QGraphicsItem::ItemIsSelectable);
}

SupportPoint::~SupportPoint()
{

}

void SupportPoint::mouseDoubleClickEvent(QGraphicsSceneMouseEvent *event)
{
    parentScene->removeItem(this);

    parentSpline->removePoint(this);
    parentSpline->draw();
}

void SupportPoint::mouseMoveEvent(QGraphicsSceneMouseEvent *event)
{
    int dist = (event->pos() - cent).manhattanLength();

    if (dist <= QApplication::startDragDistance())
    {
        return;
    }

    QPointF newPos = mapToScene(event->pos() - cent);
    setPos(newPos);

    emit pointMoved();
}

///////////////////////////////////////////////////////////////////////////////////////////////////

SplinePoint::SplinePoint(const QPointF &pt, QGraphicsScene *scene, Spline *spline) :
    Point(QRectF(pt.x() - rad, pt.y() - rad, 2 * rad, 2 * rad), scene, spline)
{
    cent = pt;

    setFlag(QGraphicsItem::ItemIsSelectable);
    setBrush(QBrush(Qt::red));
}

SplinePoint::~SplinePoint()
{

}
