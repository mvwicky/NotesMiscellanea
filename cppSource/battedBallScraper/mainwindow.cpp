#include "mainwindow.h"
#include "ui_mainwindow.h"

MainWindow::MainWindow(QWidget *parent) :
    QMainWindow(parent),
    ui(new Ui::MainWindow),
    compBase("http://gd2.mlb.com/components/game/mlb/")
{
    ui->setupUi(this);
    bool t = yearHasData(2008);
    qDebug() << t;
}



MainWindow::~MainWindow()
{
    delete ui;
}

bool MainWindow::yearHasData(const int year){
    QUrl url(compBase + "year_" + QString::number(year) + "month_04/day_01/");

    QTcpSocket socket;
    socket.connectToHost(url.host(), 80);
    if (socket.waitForConnected()){
        socket.write("HEAD" + url.path().toUtf8() + "HTTP/1.1\r\n" + "Host" + url.host().toUtf8() + "\r\n\r\n");
        if (socket.waitForReadyRead()){
            QByteArray bytes = socket.readAll();
            if (bytes.contains("200 OK"))
                return true;
        }
    }
    return false;
}
