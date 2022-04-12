#include "label.h"
#include "spline.h"

#include <QString>


ParamLabel::ParamLabel(QWidget *parent) :
    QLabel("t = " + QString::number(Spline::defaultParamValue() / 100.0), parent)
{

}

ParamLabel::~ParamLabel()
{

}

void ParamLabel::setNum(int num)
{
    setText("t = " + QString::number(num / 100.0));
}
