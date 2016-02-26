#ifndef MAINWINDOW_H
#define MAINWINDOW_H

#include <QMainWindow>

#include <QString>
#include <QFile>
#include <QList>
#include <QXmlStreamReader>
#include <QUrl>
#include <QTcpSocket>
#include <QByteArray>
#include <QTextStream>

namespace Ui {
class MainWindow;
}

class MainWindow : public QMainWindow
{
    Q_OBJECT

public:
    explicit MainWindow(QWidget *parent = 0);
    ~MainWindow();

private:
    Ui::MainWindow *ui;
    const QString compBase;
    QList<int> years;

    QString saveDir;
    QFile log;

    bool yearHasData(const int year);
    void popYears();

    void sendMessage(const QString &msg);

    int cleanAll();
    int cleanZoneMaps();
    int cleanBallMaps();
    int clearLog();
    int clearConsole();


};

#endif // MAINWINDOW_H
