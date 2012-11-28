cloudpy
=======
run python script in virtual environment on a remote platform


# Install
    $pip install cloudpy
And a config file is also needed. You can put the configurations in `/etc/cloudpy.conf`, `~/.cloudpy.conf`, or `./cloudpy.conf`.    
See the cloudpy.conf for a sample.
    
# Usage
## The easy way
    $cloudpy your_script
## The hard way
    $cloudpy -P your_script
You can do some modifications to the packed structure here

    $cloudpy -S your_package_name
Send to remote host. The package name has been return by "-P" command

    $cloudpy -R your_package_name
Run!
    
    $cloudpy -C your_package_name
Clean.


# Cloudpy

cloudpy可以将python程序（以及依赖的库和文件）打包至另一台机器，自动配置依赖的虚拟环境并实时返回结果。

cloudpy使用ssh在远程主机操作，因此需要能使用publish key 登陆ssh到远程主机。

## 安装
在本地和远程主机：    

    $ pip install cloudpy

远程主机还需要安装`virtualenv`。

## 配置
cloudpy 依次在以下位置查找配置文件：

    1. /etc/cloudpy.conf
    2. ~/.cloudpy.conf
    3. ./cloudpy.conf
    
后一项的配置会覆盖前一项。

配置文件包含一个python字典：

    {
        "host":"ubuntu@192.168.70.145",
        "depository":"cloudpy_depo",
        "host_sep":"/"
    }
    
`host`为ssh到远程主机的用户名和地址。    
`depository`为远程主机上缓存文件的目录。    
`host_sep`为远程主机目录分隔符，大多数情况下为`"/"`

## 使用
### 简单的方法:    

    $ cloudpy your_script

### 分步执行

cloudpy的执行分四步：pack、sync、run和clean。

#### Pack

pack步骤会查找脚本依赖的库、其他python文件并猜测使用到的其他文件，将之整理到合适的目录中。使用`-P` 参数执行pack过程。

    $ cloudpy -P your_script

命令返回生成的目录名称作为ID。

可以使用参数`-n name`、`-m`和`-f`.

`-n name`参数可以指定生成的目录名称。这样可以复用之前在远程机器上生成和安装好的环境。

`-m`参数指定猜测一些无法确定的库，如`snappy`包可能来自多个不同包。使用该参数将会搜索pypi以获得更多信息。对于实在无法确定包，将会在给出提示和建议。

`-f`参数制定猜测可能用到的其他文件。

##### 生成的信息文件说明
生成的以来信息在`conf/mods`中，不确定的依赖也在此文件中给出建议和可能的选项，需要手工修改指定。

#### Sync
Sync操作将Pack生成的目录同步到远程主机。`ID`为pack步骤返回的ID。

    $ cloudpy -S ID

#### Run
Run操作在远程主机执行脚本并实时返回结果。

    $ cloudpy -R ID
    
可以使用`-N`、`-c`参数。

`-N`参数输出更多的信息。包括环境的生成和配置信息。

`-c`参数在程序运行完后删除远程主机相关缓存和环境。

#### Clean
Clean操作删除本地生成的目录。

    $ cloudpy -C ID

### 参数说明
不指定具体执行步骤时，前述参数也可以使用。参数会被自动应用到对应的步骤。

如果不指定`-n name`、`-c`参数也起效。指定`-n name`参数时，不会执行Clean操作。
