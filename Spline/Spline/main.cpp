#include <QtGui/QApplication>
#include "mainwindow.h"


/// Help
/// Добавить опорную точку - щелчок мыши
/// Удалить опрную точку - двойной щелчок по точке
/// Опорные точки можно двигать
/// Параметр t меняется с помощью ползунка
/// Можно регулировать показ вспомогательных линий и линии сплайна


int main(int argc, char *argv[])
{
    QApplication a(argc, argv);
    MainWindow w;
    w.show();

    return a.exec();
}
