# sam_buy
山姆买菜

当前时间2022-04-18根据自身和身边朋友反馈正常下单，但不能保证每一个人都能成功下单.

如果此程序完全不可用，我会更新到这个位置.

时间来到了四月中下旬，居家办公也快结束了应该。在3月底开源这个项目看上去要接近尾声了.

在三月底因为抢不到绿叶菜而失落时打开了咸鱼搜索'山姆买菜'当时一个上架的商品都没有于是想自食其力搞一搞.但在今天此类商品层出不穷.

由于此开源项目间接被不遵守GPL协议的人去获利（DISS咸鱼上的卖家N次）固更新和回复不会很频繁了.

朋友们可以继续在使用 sam-buy 购买喜欢或急需的商品.

如果大家对项目有什么重大改进的话可以直接fork此项目进行修改并留言在issues中推荐给更多有需要的人用.

最后感谢@jxs0112 @guyong @Asterodeiawd 参与开发，和大家接近100star的支持.90°弯腰~

保供专用：https://github.com/guyongzx/SamsClub_buy

### 如果本工程对你有所帮助,记得点个star鼓励一下作者QAQ :)

platform: ios15;

app version: v5.0.45.1;

python version: 3.8.6;

## 更新须知
##引入configparser,requests 组件
执行
```bash

pip install --index-url https://pypi.douban.com/simple/ configparser
pip install --index-url https://pypi.douban.com/simple/ requests

```

## 有代码基础的使用v1分支,无基础使用v2
##代码中有注释，遵循注释进行修改 运行即可

# 关于配置
请修改config.ini文件
deviceid,authtoken,trackinfo三个字段为购物车的HTTP头部的字段信息

依旧没有bark支持，需要的请自行添加

# 疫情当下上海买菜太难了


关于测试：

把getCapacityData方法中唯一一句 if not 中的not去掉然后运行脚本，显示'配送时间已满'即为测试成功.

另外 测试完成后记得还原if not.

下单成功后会有音乐响起，需要自行前往app付款


## 倡导大家只够买必需品！不要浪费运力

# 仅供学习交流，不可用于非法牟利。

# 版权说明

本项目为 GPL3.0 协议，请所有进行二次开发的开发者遵守 GPL3.0协议，并且不得将代码用于商用。

本项目仅供学习交流，严禁用作商业行为，特别禁止黄牛加价代抢等！

因违法违规等不当使用导致的后果与本人无关，如有任何问题可联系本人删除！
