#include "spline.h"

#include <QDebug>
#include <QGraphicsScene>
#include <QColor>


int Spline::defaultParamValue()
{
    return defaultParam;
}


Spline::Spline(QGraphicsScene *scene) :
    points(QList<Point*>()),
    lines(QList<QGraphicsItem*>()),
    splineLines(QList<QGraphicsItem*>()),
    targetScene(scene),
    splinePoint(NULL)
{
    t = defaultParam / 100.0;
    needDrawLine = true;

    drawSplineLine = true;
    drawSupportLines = true;

    connect(this, SIGNAL(paramChanged()), this, SLOT(redraw()));
}

Spline::~Spline()
{

}

void Spline::addPoint(Point *point)
{
    points.append(point);
}

void Spline::removePoint(Point *point)
{
    points.removeOne(point);
    delete point;
}

void Spline::redraw()
{
    draw();
}

void Spline::setSplineLineStatus(int state)
{
    drawSplineLine = (state == Qt::Checked);
    needDrawLine = drawSplineLine;

    draw();
}

void Spline::setSupportLinesStaus(int state)
{
    drawSupportLines = (state == Qt::Checked);

    draw();
}

void Spline::setParam(int param)
{
    t = param / 100.0;
    needDrawLine = false;

    emit paramChanged();
}

void Spline::draw()
{
    deleteLines(lines);
    deleteSplinePoint();

    for (QList<Point*>::iterator i = points.begin(); i != points.end(); ++i)
    {
        QList<Point*>::iterator next = i + 1;

        if (next != points.end())
        {
            QPointF x = (*i)->center();
            QPointF y = (*next)->center();

            lines.append(targetScene->addLine(x.x(), x.y(), y.x(), y.y()));
        }
    }

    QList<QPointF> supportPoints = firstSupportPoints();
    drawDeCasteljau(supportPoints);

    if (!drawSplineLine)
    {
        deleteLines(splineLines);
    }
    else if (needDrawLine)
    {
        buildSplineLine();
    }
    needDrawLine = true;
}

void Spline::buildSplineLine()
{
    if (points.size() <= 2)
    {
        deleteLines(splineLines);
        return;
    }

    deleteLines(splineLines);

    QList<QPointF> splinePoints;

    for (double param = 0; param <= 1; param += 0.02)
    {
        splinePoints.append(calculateSplinePoint(param));
    }

    drawLines(splinePoints, splineLines, QPen(QBrush(Qt::red), 1));
}

void Spline::drawDeCasteljau(QList<QPointF> const& supportPoints)
{
    if (supportPoints.size() == 0)
    {
        return;
    }
    if (supportPoints.size() == 1)
    {
        splinePoint = new SplinePoint(supportPoints.at(0), targetScene, this);
        targetScene->addItem(splinePoint);

        return;
    }

    if (drawSupportLines)
    {
        drawLines(supportPoints, lines);
    }

    QList<QPointF> nextSupportPoints = calculateNextSupportPoints(supportPoints);
    drawDeCasteljau(nextSupportPoints);
}

void Spline::drawLines(QList<QPointF> const& points, QList<QGraphicsItem*>& targetBuffer, QPen const& pen)
{
    for (QList<QPointF>::const_iterator i = points.begin(); i != points.end(); ++i)
    {
        QList<QPointF>::const_iterator next = i + 1;

        if (next != points.end())
        {
            QPointF x = *i;
            QPointF y = *next;

            targetBuffer.append(targetScene->addLine(x.x(), x.y(), y.x(), y.y(), pen));
        }
    }
}

QList<QPointF> Spline::firstSupportPoints()
{
    QList<QPointF> supportPoints;

    for (QList<Point*>::iterator i = points.begin(); i != points.end(); ++i)
    {
        QList<Point*>::iterator next = i + 1;

        if (next != points.end())
        {
            QPointF x = (*i)->center();
            QPointF y = (*next)->center();

            supportPoints.append((1 - t) * x + t * y);
        }
    }

    return supportPoints;
}

QList<QPointF> Spline::calculateNextSupportPoints(const QList<QPointF> &supportPoints)
{
    QList<QPointF> nextSupportPoints;

    for (QList<QPointF>::const_iterator i = supportPoints.begin(); i != supportPoints.end(); ++i)
    {
        QList<QPointF>::const_iterator next = i + 1;

        if (next != supportPoints.end())
        {
            QPointF x = *i;
            QPointF y = *next;

            nextSupportPoints.append((1 - t) * x + t * y);
        }
    }

    return nextSupportPoints;
}

QPointF Spline::calculateSplinePoint(double param)
{
    double temp = t;
    t = param;

    QList<QPointF> supportPoints = firstSupportPoints();

    while(supportPoints.size() != 1)
    {
        supportPoints = calculateNextSupportPoints(supportPoints);
    }

    t = temp;

    return supportPoints.at(0);
}

void Spline::deleteLines(QList<QGraphicsItem*>& buffer)
{
    for (QList<QGraphicsItem*>::iterator i = buffer.begin(); i != buffer.end(); ++i)
    {
        targetScene->removeItem(*i);
        buffer.removeOne(*i);
        delete *i;
    }
}

void Spline::deleteSplinePoint()
{
    if (splinePoint == NULL)
    {
        return;
    }

    targetScene->removeItem(splinePoint);
    delete splinePoint;
}
