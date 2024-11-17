#include <iostream>
#include <boost/asio.hpp>
#include <boost/bind/bind.hpp>
#include <cmath>

using boost::asio::ip::tcp;

// 定义一个服务器类
class Server {
public:
    // 构造函数，初始化服务器并开始接受连接
    Server(boost::asio::io_context& io_context, short port)
        : acceptor_(boost::asio::make_strand(io_context), tcp::endpoint(tcp::v4(), port)) {
        start_accept();
    }

private:
    // 开始接受连接
    void start_accept() {
        // 创建一个新的 socket
        auto socket = std::make_shared<tcp::socket>(acceptor_.get_executor());
        // 异步接受连接
        acceptor_.async_accept(*socket, boost::bind(&Server::handle_accept, this, socket, boost::asio::placeholders::error));
    }

    // 处理接受到的连接
    void handle_accept(std::shared_ptr<tcp::socket> socket, const boost::system::error_code& error) {
        if (!error) {
            // 读取客户端发送的数据
            char data[1024];
            size_t length = socket->read_some(boost::asio::buffer(data));
            std::string message(data, length);

            // 解析数据，假设数据是两个浮点数
            double a, b;
            sscanf(message.c_str(), "%lf %lf", &a, &b);

            // 计算两个数的平方和的平方根
            // 这一段自己补充！

            // 将结果转换为字符串并发送回客户端
            std::string response = std::to_string(c);
            boost::asio::write(*socket, boost::asio::buffer(response));
        }
        // 继续接受下一个连接
        start_accept();
    }

    // 接受连接的对象
    tcp::acceptor acceptor_;
};

int main() {
    try {
        // 创建 io_context 对象
        boost::asio::io_context io_context;

        // 创建服务器对象，监听端口 12345（重要）
        Server server(io_context, 12345);

        // 运行 io_context，开始处理异步操作
        io_context.run();
    } catch (std::exception& e) {
        // 捕获并打印异常
        std::cerr << "Exception: " << e.what() << "\n";
    }
    return 0;
}