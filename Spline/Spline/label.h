#ifndef LABEL_H
#define LABEL_H

#include <QLabel>

class ParamLabel : public QLabel
{
    Q_OBJECT

public:
    explicit ParamLabel(QWidget *parent = NULL);
    ~ParamLabel();

public slots:
    void setNum(int num);

};

#endif // LABEL_H
