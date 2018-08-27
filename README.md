# SuperIoWatchdog-Examples


## 1. 下载


```shell
  cd ~
  mkdir SuperIoWatchDog
  cd SuperIoWatchDog
  git init
  git pull https://github.com/AplexOS/Linux-Examples.git SuperIoWatchDog:SuperIoWatchDog
```

## 2. 编译
```shell
    cd ~/SuperIoWatchDog
    make          （编译库和可执行程序）
    make libs     (编译库)
    make clean    
    cd aplex
```

## 3. 使用
```shell
    cd ~/SuperIoWatchDog/WatchDogExample
    sudo ./SuperIoWatchDog  -s          （开启看门狗，并设置默认超时时间：60s）
    sudo ./SuperIoWatchDog  -f 0x10      (开启看门狗，并设置超时时间：16s)
    sudo ./SuperIoWatchDog  -p           (关闭看门狗)
```
## 4. API
```shell
    void open_watchdog()
    功能：打开看门狗，设置默认超时时间60s

    void feed_watchdog(unsigned char time)
    功能：喂狗，设置看门狗的超时时间
    参数（time）：设置看门狗的超时时间

    void clsoe_watchdog()
    功能：关闭看门狗

```
