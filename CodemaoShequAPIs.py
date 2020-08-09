# -*- coding:utf-8 -*-
"""
**************************************************************************************************
Project Name:编程猫社区(shequ.codemao.cn)操作类
Version:1.9.0
Author:wojiaoyishang
Email:422880152@qq.com
如果你调用class中有任何疑问或建议，请通过邮箱发送给我，邮箱的主题
请以 “ #编程猫社区操作类# ” 开头并在后面跟上你的问题，如：#编程猫社区操作类# 我发现了一个BUG。

版本说明：目前版本仅支持论坛的操纵与一些基本的个人信息操纵。
**************************************************************************************************
"""
import requests, requests.utils

web = requests.session()  # 连接站点，session保持连接
User_Agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36 Edg/84.0.522.52"  # 默认浏览器标识

Version = 1.9  # 版本


class Codemao_Debug():
    """
    此类用于写Debug代码，此类为父类，请忽略！
    """

    def __init__(self, Debug):
        self.Debug = Debug
        pass

    def Debug_print(self, youid, Text):
        """
        调试输出
        """
        if self.Debug:
            print(youid + "(Debug):" + Text)


class User(Codemao_Debug):
    """
    用于操作编程猫社区中的用户信息
    详情请看 __init__ 方法 的介绍
    """

    def __init__(self, Debug=False):
        """
        此类用于操作编程猫社区中的用户信息

        参数详情：
        Debug(bool) --- 可选参数，此参数用于控制是否输出调试信息或类中出现的一些代码是否执行
        """
        # 被继承
        Codemao_Debug.__init__(self, Debug)
        # 变量
        self.myid = "Codeman.User"
        # Debug
        self.Debug_print(self.myid, "类正在初始化......")

    def login(self, Username, Password):
        """
        通过账号密码，获取用户的cookie，cookie作为用户登录到服务器的标识。
        获得cookie后在Codemao类销毁前所有子类均记录cookie
        参数详情：
        User(str) --- 提供用户名称
        Possword(str)  --- 提供用户密码

        返回:是否登录成功(bool)
        """
        global User_Agent
        try:
            headers = {"User_Agent": User_Agent,
                       "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
            data = '{"identity":"' + Username + '","password":"' + Password + '","pid":"65edCTyg"}'  # 写请求数据
            ret = web.post("https://api.codemao.cn/tiger/v3/web/accounts/login", data, headers=headers)
        except BaseException as error:
            self.Debug_print(self.myid, "登录失败原因：" + str(error))
            return False

        if ret.status_code != 200:
            self.Debug_print(self.myid, "登录失败原因：账号密码错误！")
            return False
        return True

    def get_cookie(self):
        """
        若已设置或已登录用户可返回目前正在使用的cookie

        参数说明：
        返回：cookie(str)
        """
        keys = web.cookies.keys()
        values = web.cookies.values()
        cookie = ""
        for x in range(len(keys)):
            cookie = cookie + keys[x] + "=" + values[x] + "; "
        return cookie

    def set_cookie(self, cookie):
        """
        若已有cookie，请使用此函数设置cookie状态

        参数说明：
        cookie(str) --- 已有的cookie

        返回：是否设置成功(bool)
        """
        split1 = cookie.split(";")
        cookie_dict = {}
        for i in range(len(split1)):
            split2 = split1[i].split("=")

            if len(split2) != 2:
                continue
            cookie_dict[split2[0].strip()] = split2[1].strip()
        try:
            web.cookies.update(requests.utils.cookiejar_from_dict(cookie_dict))
            return True
        except:
            return False

    def ver_cookie(self, cookie=web.cookies):
        """
        如果你需要验证此cookie是否是可以登录编程猫的，请使用此函数验证

        参数说明：
        cookie(str) --- 可选，默认使用默认的cookie

        返回：是否成功登录(bool)   若网络原因直接报错
        """

        if cookie == web.cookies:
            keys = cookie.keys()
            values = cookie.values()
            cookie = ""
            for x in range(len(keys)):
                cookie = cookie + keys[x] + "=" + values[x] + "; "
            return cookie

        headers = {"User_Agent": User_Agent, "Content-Type": "application/json;charset=UTF-8",
                   "cookies": cookie}  # 编程猫社区特有协议头，必须要有这两个
        ret = requests.get("https://shequ.codemao.cn/user/",
                           headers=headers)  # 这里不能用web.get(),web是在保持现有的连接下，我们要使用新的连接来验证 默认使用web的cookie

        if ret.status_code == 200:
            return True
        return False

    def get_my_info(self):
        """
        获取目前登录用户的信息，如果用户未登录则会返回一个空的字典，或者报错。

        返回：用户信息(dict) --- 用户的信息
        用户未设置则返回空文本
        数据key --  数据分类 -- 数据类型
        id   --  用户ID --  int
        nickname -- 用户昵称 -- str
        avatar_url -- 用户头像URL -- str
        email  --  用户邮箱 -- str
        gold   --   用户金币数 -- int
        qq   --  用户QQ  -- str
        real_name  --  用户真名 -- str
        sex   --  用户性别 -- str(男MALE  女FEMALE)
        username -- 用户名 -- str
        voice_forbidden -- 已被禁言 -- bool
        birthday -- 生日 -- int (时间戳)
        description -- 简介 -- str
        phone_number -- 加掩码的电话 -- str
        create_time -- 用户创建时间 -- int(时间戳)
        oauths -- 用户账户绑定情况 -- list(列表内有数组见下)
         |       原数据：[ {'id':1,'name':'wechat','is_bound':False} , ...]
         |       翻译： id -- 1:微信 2:QQ 3:优学派 4:国家教育资源公共服务平台 5:豹豹龙官网 6:新华文轩出版传媒 7:云知声 8.icollege远程教育平台 9.dledc? 10.apple? 11.我time网 12.中国招商银行 13:编程猫-新零售
         |              name -- 上述对应的名称     is_bound -- 是否绑定
        has_password -- 用户有密码 -- bool
        user_type -- 用户类型 -- int (未知，盲猜有普通用户、管理员之分)
        show_guide_flag  -- 展示向导标志 -- int (未知，盲猜引导页面)
        doing -- “我正在做什么”列表 -- str
        level -- 用户等级 -- int
        telephone -- 绑定电话 -- str
        """
        headers = {"User_Agent": User_Agent, "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        ret = web.get("https://api.codemao.cn/web/users/details", headers=headers)  # 返回json
        info1 = ret.json()  # 解码
        ret = web.get("https://api.codemao.cn/api/user/info", headers=headers)  # 返回json
        info2 = ret.json()  # 解码
        info1['doing'] = info2['data']['userInfo']['doing']
        info1['level'] = info2['data']['userInfo']['level']
        info1['telephone'] = info2['data']['userInfo']['telephone']
        info1['email'] = info2['data']['userInfo']['email']
        info1['qq'] = info2['data']['userInfo']['qq']
        return info1

    def get_info(self, uid):
        """
        获取别人或自己的用户信息
        如果网络原因则会触发错误

        参数说明：uid(int) -- 用户id
        返回说明：用户信息(dict) -- 返回存有用户信息的列表

        数据key --  数据分类 -- 数据类型
        isFollowing -- 我是否已关注 -- int
        collectionTimes -- 收藏数 -- int
        forkedTimes -- 再创作数 -- int
        praiseTimes -- 获赞数 -- int
        viewTimes -- 被浏览次数 -- int
        user -- 用户信息 -- dict 如下：
        |   id -- 用户id ；  nickname -- 用户昵称 ；  sex -- 性别(int 0女 1男) ； description -- 描述 ；doing -- 正在做的 ;
        |   avatar -- 头像地址 ； level -- 等级 ；preview_work_id -- 展示作品id ； preview_work_src --  展示作品地址
        work -- 展示作品详情 -- dict 如下：
        |   id -- 作品id   name -- 作品名称   preview -- 作品预览图

        """
        headers = {"User_Agent": User_Agent, "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        ret = web.get("https://api.codemao.cn/api/user/info/detail/" + str(uid), headers=headers)  # 返回json
        info = ret.json()  # 解码
        info = info['data']['userInfo']
        info['user']['description'] = info['user']['description'].replace('\\n', '\n')
        info['user']['doing'] = info['user']['doing'].replace('\\n', '\n')
        info['user']['preview_work_src'] = 'https://shequ.codemao.cn/work/' + str(info['user']['preview_work_id'])
        return info

    def set_my_info(self, nickname, sex, description, fullname, birthday, avatar_url):
        """
        更改自己的设置

        参数说明：
        nickname(str) -- 昵称
        sex(int) -- 性别(0女 1男)
        description(str) -- 描述
        fullname(str) -- 真实名称
        birthday(int) -- 生日(时间戳)
        avatar_url(str) -- 头像网址

        返回：是否成功(bool)
        """
        try:

            headers = {"User_Agent": User_Agent,
                       "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
            data = '{"nickname":"%s","description":"%s","sex": %d,"fullname":"%s","birthday": %d,"avatar_url":"%s"}' \
                   % (nickname,description,sex,fullname,birthday,avatar_url)

            ret = web.patch('https://api.codemao.cn/tiger/v3/web/accounts/info',
                            data=data.encode('utf-8'), headers=headers)

            if ret.status_code != 204:
                self.Debug_print(self.myid, ret.text)
                return False
            return True
        except BaseException as error:
            self.Debug_print(self.myid, str(error))
            return False


class Community(Codemao_Debug):
    """
    用于操作编程猫社区中的论坛
    详情请看 __init__ 方法 的介绍
    """

    def __init__(self, Debug=False):
        """
        此类用于操作编程猫社区中的论坛

        前排提示：编程猫论坛的楼主评论和回复评论有实质的区别，楼主评论以 replies 表示，回复评论以 comments 表示。

        参数详情：
        Debug(bool) --- 可选参数，此参数用于控制是否输出调试信息或类中出现的一些代码是否执行
        """
        # 被继承
        Codemao_Debug.__init__(self, Debug)
        self.Debug_print("Codeman.Community", "正在初始化......")

    def get_post_info(self, post_id):
        """
        获取文章标准信息，获取时会增加文章访问量

        参数说明：post_id(int) -- 帖子的ID

        返回:帖子信息(dict) -- 返回帖子字典

        帖子不存在时：
        数据key --  数据分类 -- 数据类型
        error_code -- 错误代码 -- str
        error_message -- 错误信息 -- str
        log_uuid -- 用户登录uuid -- str
        domain -- ??? -- list

        帖子存在时：
        数据key --  数据分类 -- 数据类型
        id -- 帖子id -- int
        title -- 帖子标题 -- str
        content -- 帖子内容(HTML) -- str
        board_id -- 分区id -- int
        board_name -- 分区名称 -- str
        updated_at -- 更新时间 -- int(时间戳)
        created_at -- 创建时间 -- int(时间戳)
        n_views -- 帖子访问量 -- int
        n_replies -- 评论回复数 -- int
        n_comments -- 评论数(楼主) -- int
        is_authorized -- 被授权的文章 -- bool
        is_featured -- 有特色的文章? -- bool
        is_hotted -- 热门的文章 -- bool
        is_pinned -- 置顶的文章 -- bool
        tutorial_flag -- 被辅导标志 -- int
        ask_help_flag -- 求助标志 -- int
        user -- 帖子用户信息 -- dict
        |   id -- 用户id ； nickname -- 用户名称 ； avatar_url -- 用户头像 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        """

        headers = {"User_Agent": User_Agent, "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        ret = web.get("https://api.codemao.cn/web/forums/posts/" + str(post_id) + "/details",
                      headers=headers)  # 返回json
        return ret.json()

    def get_post_comment(self, post_id):
        """
        获取文章的全部评论，获取时会增加文章访问量

        参数说明：post_id(int) -- 帖子的ID

        返回：评论(list) -- 评论,每一个项中都存储了一个评论数据(dict)，评论数据如下分析：

        数据key --  数据分类 -- 数据类型
        id -- 用户id -- int
        is_top -- 评论被置顶 -- bool
        n_likes -- 点赞数 -- int
        is_liked -- 我喜欢 -- bool
        content -- 评论内容(html) -- str
        n_comments -- 回复评论数 -- int
        updated_at -- 更新时间 -- int(时间戳)
        created_at -- 创建时间 -- int(时间戳)
        earliest_comments -- 回复的评论 -- dict(与上述一致)

        """
        count = self.get_post_info(post_id)['n_comments'] // 30
        if self.get_post_info(post_id)['n_comments'] % 30 != 0:
            count += 1
        comment = []
        for x in range(count):
            ret = web.get(f'https://api.codemao.cn/web/forums/posts/{post_id}/replies?page={x + 1}&limit=30')
            comment = comment + ret.json()['items']

        return comment

    def replie(self, post_id, html):
        """
        评论帖子，不是回复评论，回复别人使用 comments() 方法

        参数说明：
        post_id(int) -- 帖子ID
        html(str) -- 回复的内容 请用html代码

        返回：评论id(int) -- 成功返回评论ID，失败返回0
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        ret = web.post(f'https://api.codemao.cn/web/forums/posts/{post_id}/replies',
                       data=('{"content":"' + html + '"}').encode('utf-8'), headers=headers)
        if ret.status_code != 201:
            return 0
        return ret.json()['id']

    def replie_del(self, replies_id):
        """
        删除楼主评论

        参数说明：replies_id -- 楼主评论

        返回是否成功(bool)
        """
        try:
            headers = {"User_Agent": User_Agent,
                       "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
            if web.delete(f'https://api.codemao.cn/web/forums/replies/' + str(replies_id),
                          headers=headers).status_code != 204:
                return False

            return True
        except:
            return False

    def comment(self, replies_id, html, comments_id=0):
        """
        回复楼主或者是回复其它人，不是回复帖子评论，回复帖子使用 replies() 方法

        参数说明：
        replies_id(int) -- 楼主评论ID
        comments_id(int) -- 可选 如果楼主下面还有人回复，你想要回复那个人，请提供他的id，没有默认为 0
        html(str) -- 回复的内容 请用html代码

        返回：评论id(int) -- 成功返回评论ID，失败返回0
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        ret = web.post(f'https://api.codemao.cn/web/forums/replies/{replies_id}/comments',
                       data=('{"parent_id":' + str(comments_id) + ',"content":"' + html + '"}').encode('utf-8'),
                       headers=headers)
        if ret.status_code != 201:
            return 0
        return ret.json()['id']

    def comment_del(self, comments_id):
        """
        删除回复评论

        参数说明：comments_id -- 回复评论ID

        返回是否成功(bool)
        """
        try:
            headers = {"User_Agent": User_Agent,
                       "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
            if web.delete(f'https://api.codemao.cn/web/forums/comment/' + str(comments_id),
                          headers=headers).status_code != 204:
                return False

            return True
        except:
            return False

    def replies_like(self, replies_id):
        """
        为楼主的评论点赞，注意是楼主评论不是回复评论，回复评论请使用 comments_like() 方法

        参数说明：replies_id(int) -- 楼主评论id

        返回：是否成功(bool)
        """
        try:
            headers = {"User_Agent": User_Agent,
                       "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
            web.put(f'https://api.codemao.cn/web/forums/comments/{replies_id}/liked?source=REPLY', data="{}",
                    headers=headers)
            return True
        except:
            return False

    def replies_diss_like(self, replies_id):
        """
        为楼主的评论取消点赞，注意是楼主评论不是回复评论，回复评论请使用 comments_diss_like() 方法

        参数说明：replies_id(int) -- 楼主评论id

        返回：是否成功(bool)
        """
        try:
            headers = {"User_Agent": User_Agent,
                       "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
            web.delete(f'https://api.codemao.cn/web/forums/comments/{replies_id}/liked?source=REPLY',
                       data="source=REPLY", headers=headers)
            return True
        except:
            return False

    def comment_like(self, comments_id):
        """
        为回复的评论点赞，注意是回复评论不是楼主评论，回复评论请使用 replies_like() 方法

        参数说明：replies_id(int) -- 楼主评论id

        返回：是否成功(bool)
        """
        try:
            headers = {"User_Agent": User_Agent,
                       "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
            if web.put(f'https://api.codemao.cn/web/forums/comments/{comments_id}/liked?source=comments', data="{}",
                       headers=headers).status_code != 204:
                return False

            return True
        except:
            return False

    def comment_diss_like(self, comments_id):
        """
        为回复的评论取消点赞，注意是回复评论不是楼主评论，回复评论请使用 replies_like() 方法

        参数说明：replies_id(int) -- 楼主评论id

        返回：是否成功(bool)
        """
        try:
            headers = {"User_Agent": User_Agent,
                       "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
            if web.delete(f'https://api.codemao.cn/web/forums/comments/{comments_id}/liked?source=comments',
                          data="source=REPLY", headers=headers) != 204:
                return False

            return True
        except:
            return False

    def get_my_replies_post(self):
        """
        获取我评论的帖子

        返回：返回我评论的帖子的数据(list) -- 帖子数据 每一个列表中含有一个字典，字典结构如下

        数据key --  数据分类 -- 数据类型
        id -- 帖子id -- int
        title -- 帖子标题 -- str
        content -- 帖子摘要(HTML) -- str
        created_at -- 创建时间 -- int(时间戳)
        n_replies -- 评论回复数 -- int
        n_comments -- 评论数(楼主) -- int
        is_authorized -- 被授权的文章 -- bool
        is_featured -- 有特色的文章? -- bool
        is_hotted -- 热门的文章 -- bool
        is_pinned -- 置顶的文章 -- bool
        tutorial_flag -- 被辅导标志 -- int
        ask_help_flag -- 求助标志 -- int
        user -- 帖子用户信息 -- dict
        |   id -- 用户id ； nickname -- 用户名称 ； avatar_url -- 用户头像 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        commented_at -- 评论时间 -- int(时间戳)
        commented_user -- 评论用户信息 -- dict 如下：
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        replied_at -- 最新回复（非自己回复） -- int(时间戳)
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        ret1 = web.get('https://api.codemao.cn/web/forums/posts/mine/replied?page=1&limit=30', headers=headers)
        total = ret1.json()['total']
        count = total // 30
        if total % 30 != 0:
            count += 1
        replies = []

        for x in range(count):
            ret1 = web.get(f'https://api.codemao.cn/web/forums/posts/mine/replied?page={x + 1}&limit=30',
                           headers=headers)

            replies = replies + ret1.json()['items']
        return replies

    def get_my_release_post(self):
        """
        获取我发布的帖子

        返回：返回我发布帖子的数据(list) -- 帖子数据 每一个列表中含有一个字典，字典结构如下

        数据key --  数据分类 -- 数据类型
        id -- 帖子id -- int
        title -- 帖子标题 -- str
        content -- 帖子摘要(HTML) -- str
        created_at -- 创建时间 -- int(时间戳)
        n_replies -- 评论回复数 -- int
        n_comments -- 评论数(楼主) -- int
        is_authorized -- 被授权的文章 -- bool
        is_featured -- 有特色的文章? -- bool
        is_hotted -- 热门的文章 -- bool
        is_pinned -- 置顶的文章 -- bool
        tutorial_flag -- 被辅导标志 -- int
        ask_help_flag -- 求助标志 -- int
        user -- 帖子用户信息 -- dict
        |   id -- 用户id ； nickname -- 用户名称 ； avatar_url -- 用户头像 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        commented_at -- 评论时间 -- int(时间戳)
        commented_user -- 评论用户信息 -- dict 如下：
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        replied_at -- 最新回复（非自己回复） -- int(时间戳)
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        ret1 = web.get('https://api.codemao.cn/web/forums/posts/mine/created?page=1&limit=30', headers=headers)
        total = ret1.json()['total']
        count = total // 30
        if total % 30 != 0:
            count += 1
        replies = []

        for x in range(count):
            ret1 = web.get(f'https://api.codemao.cn/web/forums/posts/mine/created?page={x + 1}&limit=30',
                           headers=headers)

            replies = replies + ret1.json()['items']
        return replies

    def get_latest_replies_post(self):
        """
        获取首页最新回复文章id，包括置顶文章共300个

        返回：列表(list) -- 每一个项都是文章id
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        ret = web.get('https://api.codemao.cn/web/forums/posts/hots/all', headers=headers)
        return ret.json()['items']

    def get_post_easy_info(self, post_ids):
        """
        获取文章简单信息，与 get_post_info 不同的是会获取最新回复
        匹配数量不要 >30

        参数说明：
        post_ids -- 允许正则表达式，也允许传入列表，列表内包含文章id
        返回：文章信息(list) -- 批量文章信息，每一个项都是文章标准信息 如下

        数据key --  数据分类 -- 数据类型
        id -- 帖子id -- int
        title -- 帖子标题 -- str
        content -- 帖子摘要(HTML) -- str
        created_at -- 创建时间 -- int(时间戳)
        n_replies -- 评论回复数 -- int
        n_comments -- 评论数(楼主) -- int
        is_authorized -- 被授权的文章 -- bool
        is_featured -- 有特色的文章? -- bool
        is_hotted -- 热门的文章 -- bool
        is_pinned -- 置顶的文章 -- bool
        tutorial_flag -- 被辅导标志 -- int
        ask_help_flag -- 求助标志 -- int
        user -- 帖子用户信息 -- dict
        |   id -- 用户id ； nickname -- 用户名称 ； avatar_url -- 用户头像 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        commented_at -- 评论时间 -- int(时间戳)
        commented_user -- 评论用户信息 -- dict 如下：
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        replied_at -- 最新回复（非自己回复） -- int(时间戳)
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        """

        if isinstance(post_ids, list):
            total = len(post_ids)
            count = 0
            ret_list = []
            while count < total:

                post_ids2 = post_ids[count:count + 29]
                post_ids2 = str(post_ids2).replace('[', '').replace(']', '').replace('\'', '').replace(' ', '')
                headers = {"User_Agent": User_Agent,
                           "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
                ret = web.get('https://api.codemao.cn/web/forums/posts/all?ids=' + post_ids2, headers=headers)
                ret_list = ret_list + ret.json()['items']
                count += 30
                if count > total:
                    count = total
            return ret_list

        else:
            headers = {"User_Agent": User_Agent,
                       "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
            ret = web.get('https://api.codemao.cn/web/forums/posts/all?ids=' + post_ids, headers=headers)
            return ret.json()['items']

    def get_7dayHot_post(self, total, board_id=""):
        """
        获取七日热门文章 返回文章信息，不是文章id

        参数说明：
        total -- 获取数量
        board_id -- 可选参数，不指定请留空，如下：
        |    1 -- 点猫看板 ； 2 -- 积木编程乐园 ； 3 -- 代码岛 ； 4 -- 通天塔 ；  5 -- 你问我答 ； 6 -- 动漫小说 ；
        |    7 -- 灌水池塘 ； 8 -- 我要提建议   ； 9 -- 作品秀 ；10 -- 工作室 ； 11 -- Python乐园 ； 12 -- 求素材；
        |    13 -- NOC编程猫比赛 ； 15 -- UnderTale ； 16 -- I wanna ； 17 -- 热门活动  ； 18 -- Scratch专区 ；
        |    19 -- 动作游戏专区 ； 20 -- 射击游戏专区 ； 21 -- 休闲游戏专区 ；22 -- 学术作品专区 ；23 -- 艺术作品专区 ；
        |    24 -- 工作室招新； 25 -- 师徒广场 ； 26 -- 源码精灵

        返回：文章信息(list) -- 文章信息,每一个项都是文章标准信息 如下

        数据key --  数据分类 -- 数据类型
        id -- 帖子id -- int
        title -- 帖子标题 -- str
        content -- 帖子摘要(HTML) -- str
        created_at -- 创建时间 -- int(时间戳)
        n_replies -- 评论回复数 -- int
        n_comments -- 评论数(楼主) -- int
        is_authorized -- 被授权的文章 -- bool
        is_featured -- 有特色的文章? -- bool
        is_hotted -- 热门的文章 -- bool
        is_pinned -- 置顶的文章 -- bool
        tutorial_flag -- 被辅导标志 -- int
        ask_help_flag -- 求助标志 -- int
        user -- 帖子用户信息 -- dict
        |   id -- 用户id ； nickname -- 用户名称 ； avatar_url -- 用户头像 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        commented_at -- 评论时间 -- int(时间戳)
        commented_user -- 评论用户信息 -- dict 如下：
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        replied_at -- 最新回复（非自己回复） -- int(时间戳)
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个

        count = total // 30
        if total % 30 != 0:
            count += 1
        replies = []
        add = ""
        if board_id == "":
            add = f"&board_id={board_id}"
        for x in range(count):
            if x == count - 1 and total % 30 != 0:
                i = total % 30
                if i < 5:
                    i = 5
                ret1 = web.get(
                    f'https://api.codemao.cn/web/forums/boards/posts/7dayHot?page={x + 1}&limit=' + str(i) + add,
                    headers=headers)
            else:
                ret1 = web.get(
                    f'https://api.codemao.cn/web/forums/boards/posts/7dayHot?page={x + 1}&limit=30' + add,
                    headers=headers)

            replies = replies + ret1.json()['items']
        return replies

    def get_7datHot_many(self, board_id=""):
        """
        获取七日热门文章总数

        board_id -- 可选参数，不指定请留空，如下：
        |    1 -- 点猫看板 ； 2 -- 积木编程乐园 ； 3 -- 代码岛 ； 4 -- 通天塔 ；  5 -- 你问我答 ； 6 -- 动漫小说 ；
        |    7 -- 灌水池塘 ； 8 -- 我要提建议   ； 9 -- 作品秀 ；10 -- 工作室 ； 11 -- Python乐园 ； 12 -- 求素材；
        |    13 -- NOC编程猫比赛 ； 15 -- UnderTale ； 16 -- I wanna ； 17 -- 热门活动  ； 18 -- Scratch专区 ；
        |    19 -- 动作游戏专区 ； 20 -- 射击游戏专区 ； 21 -- 休闲游戏专区 ；22 -- 学术作品专区 ；23 -- 艺术作品专区 ；
        |    24 -- 工作室招新； 25 -- 师徒广场 ； 26 -- 源码精灵

        返回：总数(int) -- 文章总数
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        add = ""
        if board_id == "":
            add = f"&board_id={board_id}"
        ret1 = web.get(f'https://api.codemao.cn/web/forums/boards/posts/7dayHot?page=1&limit=30' + add,
                       headers=headers)

        return ret1.json()['total']

    def get_selections_post(self, total, board_id=""):
        """
        获取精品合集文章 返回文章信息，不是文章id

        参数说明：
        total -- 获取数量
        board_id -- 可选参数，不指定请留空，如下：
        |    1 -- 点猫看板 ； 2 -- 积木编程乐园 ； 3 -- 代码岛 ； 4 -- 通天塔 ；  5 -- 你问我答 ； 6 -- 动漫小说 ；
        |    7 -- 灌水池塘 ； 8 -- 我要提建议   ； 9 -- 作品秀 ；10 -- 工作室 ； 11 -- Python乐园 ； 12 -- 求素材；
        |    13 -- NOC编程猫比赛 ； 15 -- UnderTale ； 16 -- I wanna ； 17 -- 热门活动  ； 18 -- Scratch专区 ；
        |    19 -- 动作游戏专区 ； 20 -- 射击游戏专区 ； 21 -- 休闲游戏专区 ；22 -- 学术作品专区 ；23 -- 艺术作品专区 ；
        |    24 -- 工作室招新； 25 -- 师徒广场 ； 26 -- 源码精灵

        返回：文章信息(dict) -- 文章信息 如下

        数据key --  数据分类 -- 数据类型
        id -- 帖子id -- int
        title -- 帖子标题 -- str
        content -- 帖子摘要(HTML) -- str
        created_at -- 创建时间 -- int(时间戳)
        n_replies -- 评论回复数 -- int
        n_comments -- 评论数(楼主) -- int
        is_authorized -- 被授权的文章 -- bool
        is_featured -- 有特色的文章? -- bool
        is_hotted -- 热门的文章 -- bool
        is_pinned -- 置顶的文章 -- bool
        tutorial_flag -- 被辅导标志 -- int
        ask_help_flag -- 求助标志 -- int
        user -- 帖子用户信息 -- dict
        |   id -- 用户id ； nickname -- 用户名称 ； avatar_url -- 用户头像 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        commented_at -- 评论时间 -- int(时间戳)
        commented_user -- 评论用户信息 -- dict 如下：
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        replied_at -- 最新回复（非自己回复） -- int(时间戳)
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章

        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个

        count = total // 30
        if total % 30 != 0:
            count += 1
        replies = []
        add = ""
        if board_id == "":
            add = f"&board_id={board_id}"
        for x in range(count):

            if x == count - 1 and total % 30 != 0:
                i = total % 30
                if i < 5:
                    i = 5
                ret1 = web.get(
                    f'https://api.codemao.cn/web/forums/boards/posts/selections?page={x + 1}&limit=' + str(
                        i) + add,
                    headers=headers)
            else:
                ret1 = web.get(f'https://api.codemao.cn/web/forums/boards/posts/selections?page={x + 1}&limit=30' + add,
                               headers=headers)
            replies = replies + ret1.json()['items']
        return replies

    def get_selections_many(self, board_id=""):
        """
        获取精品合集文章总数

        board_id -- 可选参数，不指定请留空，如下：
        |    1 -- 点猫看板 ； 2 -- 积木编程乐园 ； 3 -- 代码岛 ； 4 -- 通天塔 ；  5 -- 你问我答 ； 6 -- 动漫小说 ；
        |    7 -- 灌水池塘 ； 8 -- 我要提建议   ； 9 -- 作品秀 ；10 -- 工作室 ； 11 -- Python乐园 ； 12 -- 求素材；
        |    13 -- NOC编程猫比赛 ； 15 -- UnderTale ； 16 -- I wanna ； 17 -- 热门活动  ； 18 -- Scratch专区 ；
        |    19 -- 动作游戏专区 ； 20 -- 射击游戏专区 ； 21 -- 休闲游戏专区 ；22 -- 学术作品专区 ；23 -- 艺术作品专区 ；
        |    24 -- 工作室招新； 25 -- 师徒广场 ； 26 -- 源码精灵

        返回：总数(int) -- 文章总数
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        add = ""
        if board_id == "":
            add = f"&board_id={board_id}"
        ret1 = web.get('https://api.codemao.cn/web/forums/boards/posts/selections?page=1&limit=30' + add,
                       headers=headers)
        return ret1.json()['total']

    def get_ask_help_post(self, total, board_id=""):
        """
        获取求帮助文章 返回文章信息，不是文章id

        参数说明：
        total -- 获取数量
        board_id -- 可选参数，不指定请留空，如下：
        |    1 -- 点猫看板 ； 2 -- 积木编程乐园 ； 3 -- 代码岛 ； 4 -- 通天塔 ；  5 -- 你问我答 ； 6 -- 动漫小说 ；
        |    7 -- 灌水池塘 ； 8 -- 我要提建议   ； 9 -- 作品秀 ；10 -- 工作室 ； 11 -- Python乐园 ； 12 -- 求素材；
        |    13 -- NOC编程猫比赛 ； 15 -- UnderTale ； 16 -- I wanna ； 17 -- 热门活动  ； 18 -- Scratch专区 ；
        |    19 -- 动作游戏专区 ； 20 -- 射击游戏专区 ； 21 -- 休闲游戏专区 ；22 -- 学术作品专区 ；23 -- 艺术作品专区 ；
        |    24 -- 工作室招新； 25 -- 师徒广场 ； 26 -- 源码精灵
        返回：文章信息(dict) -- 文章信息 如下

        数据key --  数据分类 -- 数据类型
        id -- 帖子id -- int
        title -- 帖子标题 -- str
        content -- 帖子摘要(HTML) -- str
        created_at -- 创建时间 -- int(时间戳)
        n_replies -- 评论回复数 -- int
        n_comments -- 评论数(楼主) -- int
        is_authorized -- 被授权的文章 -- bool
        is_featured -- 有特色的文章? -- bool
        is_hotted -- 热门的文章 -- bool
        is_pinned -- 置顶的文章 -- bool
        tutorial_flag -- 被辅导标志 -- int
        ask_help_flag -- 求助标志 -- int
        user -- 帖子用户信息 -- dict
        |   id -- 用户id ； nickname -- 用户名称 ； avatar_url -- 用户头像 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        commented_at -- 评论时间 -- int(时间戳)
        commented_user -- 评论用户信息 -- dict 如下：
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        replied_at -- 最新回复（非自己回复） -- int(时间戳)
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个

        count = total // 30
        if total % 30 != 0:
            count += 1
        replies = []
        add = ""
        if board_id == "":
            add = f"&board_id={board_id}"
        for x in range(count):

            if x == count - 1 and total % 30 != 0:
                i = total % 30
                if i < 5:
                    i = 5
                ret1 = web.get(
                    f'https://api.codemao.cn/web/forums/boards/posts/ask-help?page={x + 1}&limit=' + str(
                        i) + add,
                    headers=headers)
            else:
                ret1 = web.get(f'https://api.codemao.cn/web/forums/boards/posts/ask-help?page={x + 1}&limit=30' + add,
                               headers=headers)
            replies = replies + ret1.json()['items']
        return replies

    def get_ask_help_many(self, board_id=""):
        """
        获取求帮助文章总数
        board_id -- 可选参数，不指定请留空，如下：
        |    1 -- 点猫看板 ； 2 -- 积木编程乐园 ； 3 -- 代码岛 ； 4 -- 通天塔 ；  5 -- 你问我答 ； 6 -- 动漫小说 ；
        |    7 -- 灌水池塘 ； 8 -- 我要提建议   ； 9 -- 作品秀 ；10 -- 工作室 ； 11 -- Python乐园 ； 12 -- 求素材；
        |    13 -- NOC编程猫比赛 ； 15 -- UnderTale ； 16 -- I wanna ； 17 -- 热门活动  ； 18 -- Scratch专区 ；
        |    19 -- 动作游戏专区 ； 20 -- 射击游戏专区 ； 21 -- 休闲游戏专区 ；22 -- 学术作品专区 ；23 -- 艺术作品专区 ；
        |    24 -- 工作室招新； 25 -- 师徒广场 ； 26 -- 源码精灵
        返回：总数(int) -- 文章总数
        """
        add = ""
        if board_id == "":
            add = f"&board_id={board_id}"
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        ret1 = web.get('https://api.codemao.cn/web/forums/boards/posts/ask-help?page=1&limit=30' + add, headers=headers)
        return ret1.json()['total']

    def search_post(self, key, total):
        """
        获取搜索内容

        参数说明：
        key(str) -- 搜索内容
        total(int) -- 搜索数量

        返回：文章信息(dict) -- 文章信息 如下

        数据key --  数据分类 -- 数据类型
        id -- 帖子id -- int
        title -- 帖子标题 -- str
        content -- 帖子摘要(HTML) -- str
        created_at -- 创建时间 -- int(时间戳)
        n_replies -- 评论回复数 -- int
        n_comments -- 评论数(楼主) -- int
        is_authorized -- 被授权的文章 -- bool
        is_featured -- 有特色的文章? -- bool
        is_hotted -- 热门的文章 -- bool
        is_pinned -- 置顶的文章 -- bool
        tutorial_flag -- 被辅导标志 -- int
        ask_help_flag -- 求助标志 -- int
        user -- 帖子用户信息 -- dict
        |   id -- 用户id ； nickname -- 用户名称 ； avatar_url -- 用户头像 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        commented_at -- 评论时间 -- int(时间戳)
        commented_user -- 评论用户信息 -- dict 如下：
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        replied_at -- 最新回复（非自己回复） -- int(时间戳)
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个

        count = total // 30
        if total % 30 != 0:
            count += 1
        replies = []

        for x in range(count):
            if x == count - 1 and total % 30 != 0:
                i = total % 30
                if i < 5:
                    i = 5
                ret1 = web.get(
                    f'https://api.codemao.cn/web/forums/posts/search?title={key}&page={x + 1}&limit=' + str(
                        i),
                    headers=headers)
            else:
                ret1 = web.get(f'https://api.codemao.cn/web/forums/posts/search?title={key}&page={x + 1}&limit=30',
                               headers=headers)
            replies = replies + ret1.json()['items']
        return replies

    def get_search_post_many(self, key):
        """
        获取搜索总数
        参数：key(str) -- 搜索字符
        返回：总数(int) -- 文章总数
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        ret1 = web.get('https://api.codemao.cn/web/forums/posts/search?title=' + key, headers=headers)
        return ret1.json()['total']

    def get_board_info(self, board_id):
        """
        获取版块信息，

        参数说明：
        board_id(int) -- 版块ID ，版块ID如下：
        |    1 -- 点猫看板 ； 2 -- 积木编程乐园 ； 3 -- 代码岛 ； 4 -- 通天塔 ；  5 -- 你问我答 ； 6 -- 动漫小说 ；
        |    7 -- 灌水池塘 ； 8 -- 我要提建议   ； 9 -- 作品秀 ；10 -- 工作室 ； 11 -- Python乐园 ； 12 -- 求素材；
        |    13 -- NOC编程猫比赛 ； 15 -- UnderTale ； 16 -- I wanna ； 17 -- 热门活动  ； 18 -- Scratch专区 ；
        |    19 -- 动作游戏专区 ； 20 -- 射击游戏专区 ； 21 -- 休闲游戏专区 ；22 -- 学术作品专区 ；23 -- 艺术作品专区 ；
        |    24 -- 工作室招新； 25 -- 师徒广场 ； 26 -- 源码精灵

        返回：版块信息(dcit) -- 版块信息字典 如下：

        不存在版块：
        数据key --  数据分类 -- 数据类型
        error_code -- 错误代码 -- str
        error_message -- 错误信息 -- str
        log_uuid -- 用户登录uuid -- str

        存在版块：
        数据key -- 数据说明 -- 数据类型
        id -- 版块ID -- int
        name -- 版块名称 -- str
        description -- 版块简介 -- str
        icon_url -- 版块图片网址 -- str
        is_hot -- 版块是否热门 -- bool
        has_popular -- 版块是否流行 -- bool
        has_selection -- 版块是否被选拔? -- bool
        n_posts -- 版块帖子数 -- int
        n_discussions -- 版块讨论数 -- int
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        ret1 = web.get('https://api.codemao.cn/web/forums/boards/' + str(board_id), headers=headers)
        return ret1.json()

    def get_board_post_info(self, board_id, total):
        """
        获取某版块文章，

        参数说明：
        board_id(int) -- 版块ID ，版块ID如下：
        |    1 -- 点猫看板 ； 2 -- 积木编程乐园 ； 3 -- 代码岛 ； 4 -- 通天塔 ；  5 -- 你问我答 ； 6 -- 动漫小说 ；
        |    7 -- 灌水池塘 ； 8 -- 我要提建议   ； 9 -- 作品秀 ；10 -- 工作室 ； 11 -- Python乐园 ； 12 -- 求素材；
        |    13 -- NOC编程猫比赛 ； 15 -- UnderTale ； 16 -- I wanna ； 17 -- 热门活动  ； 18 -- Scratch专区 ；
        |    19 -- 动作游戏专区 ； 20 -- 射击游戏专区 ； 21 -- 休闲游戏专区 ；22 -- 学术作品专区 ；23 -- 艺术作品专区 ；
        |    24 -- 工作室招新； 25 -- 师徒广场 ； 26 -- 源码精灵
        total(int) -- 获取数量（一共有多少文章请用 get_board_info() 方法）

        返回：文章信息(dict) -- 文章信息 如下

        数据key --  数据分类 -- 数据类型
        id -- 帖子id -- int
        title -- 帖子标题 -- str
        content -- 帖子摘要(HTML) -- str
        created_at -- 创建时间 -- int(时间戳)
        n_replies -- 评论回复数 -- int
        n_comments -- 评论数(楼主) -- int
        is_authorized -- 被授权的文章 -- bool
        is_featured -- 有特色的文章? -- bool
        is_hotted -- 热门的文章 -- bool
        is_pinned -- 置顶的文章 -- bool
        tutorial_flag -- 被辅导标志 -- int
        ask_help_flag -- 求助标志 -- int
        user -- 帖子用户信息 -- dict
        |   id -- 用户id ； nickname -- 用户名称 ； avatar_url -- 用户头像 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        commented_at -- 评论时间 -- int(时间戳)
        commented_user -- 评论用户信息 -- dict 如下：
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        replied_at -- 最新回复（非自己回复） -- int(时间戳)
        |   id -- 评论用户id ； nickname -- 用户昵称 ； avatar_url -- 头像地址 ； subject_id -- 课程id ；
        |   work_shop_name -- 参加工作室的名称 ； work_shop_level -- 工作室等级 ; wuhan_medal -- 拥有武汉奖章
        """

        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个

        count = total // 30
        if total % 30 != 0:
            count += 1
        replies = []

        for x in range(count):

            if x == count - 1 and total % 30 != 0:
                i = total % 30
                if i < 5:
                    i = 5
                ret1 = web.get(
                    f'https://api.codemao.cn/web/forums/boards/{board_id}/posts?&page={x + 1}&limit=' + str(i),
                    headers=headers)
            else:
                ret1 = web.get(f'https://api.codemao.cn/web/forums/boards/{board_id}/posts?&page={x + 1}&limit=30',
                               headers=headers)

            replies = replies + ret1.json()['items']
        return replies

    def reports_post(self, post_id, reports_id, reports_description):
        """
        举报文章，不是举报评论

        参数说明：
        post_id(int) -- 举报的文章ID
        reports_id(int) -- 举报分区，如下：
        |   1 -- 违法违规 ； 2 -- 色情暴力 ； 3 -- 侵犯隐私 ； 4 -- 人身攻击 ； 5 -- 引战 ；
        |   6 -- 垃圾广告 ； 7 -- 无意义刷屏 ； 8 -- 不良信息
        reports_description(str) -- 举报描述 （非html代码）

        举报成功返回ID，失败或已举报过则报错。
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个

        ret = web.post('https://api.codemao.cn/web/reports/posts', data=(
                    '{"post_id":"' + str(post_id) + '","reason_id":"' + str(
                reports_id) + '","description":"' + reports_description + '"}').encode('utf-8'), headers=headers)

        return ret.json()['id']
    def reports_discussions(self,discussions_id,reports_id,reports_description=""):
        """
        举报评论

        参数说明：
        discussions_id(int) -- 评论ID
        reports_id(int) -- 举报分区，如下：
        |   1 -- 违法违规 ； 2 -- 色情暴力 ； 3 -- 侵犯隐私 ； 4 -- 人身攻击 ； 5 -- 引战 ；
        |   6 -- 垃圾广告 ； 7 -- 无意义刷屏 ； 8 -- 不良信息 ； 0 -- 自定义（须填写内容）
        reports_description -- 举报描述 reports_id选择0时必须填写 选择其它不填写

        返回：举报ID
        """
        if reports_id != 0 and reports_description != "":
            raise BaseException("当reports_id不为0时，reports_description不可填写")
        elif reports_id == 0 and  reports_description == "":
            raise BaseException("当reports_id为0时，reports_description必须填写")
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
        if reports_id == 0:
            data = '{"discussion_id":"%d","source":"REPLY","reason_id":"%d","description":"%s"}'%(discussions_id,reports_id,reports_description)
        else:
            data = '{"discussion_id":"%d","source":"REPLY","reason_id":"%d"}'%(discussions_id,reports_id)

        ret = web.post('https://api.codemao.cn/web/reports/posts/discussions', data=(data).encode('utf-8'), headers=headers)

        return ret.json()['id']

    def post(self, board_id, post_title, post_html):
        """
        发布文章

        参数说明：
        board_id(int) -- 版块ID ，版块ID如下：
        |    1 -- 点猫看板 ； 2 -- 积木编程乐园 ； 3 -- 代码岛 ； 4 -- 通天塔 ；  5 -- 你问我答 ； 6 -- 动漫小说 ；
        |    7 -- 灌水池塘 ； 8 -- 我要提建议   ； 9 -- 作品秀 ；10 -- 工作室 ； 11 -- Python乐园 ； 12 -- 求素材；
        |    13 -- NOC编程猫比赛 ； 15 -- UnderTale ； 16 -- I wanna ； 17 -- 热门活动  ； 18 -- Scratch专区 ；
        |    19 -- 动作游戏专区 ； 20 -- 射击游戏专区 ； 21 -- 休闲游戏专区 ；22 -- 学术作品专区 ；23 -- 艺术作品专区 ；
        |    24 -- 工作室招新； 25 -- 师徒广场 ； 26 -- 源码精灵
        post_title(str) -- 文章标题 5~50字
        post_html(str) -- 文章内容(html)

        发布成功返回文章id，失败报错
        """
        headers = {"User_Agent": User_Agent,
                   "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个

        ret = web.post(f'https://api.codemao.cn/web/forums/boards/{board_id}/posts',
                       data=('{"title":"' + post_title + '","content":"' + post_html + '"}').encode('utf-8'),
                       headers=headers)

        return ret.json()['id']

    def post_del(self, post_id):
        """
        删除文章

        参数说明：post_id(int) -- 文章id

        返回：是否成功(bool)
        """
        try:
            headers = {"User_Agent": User_Agent,
                       "Content-Type": "application/json;charset=UTF-8"}  # 编程猫社区特有协议头，必须要有这两个
            if web.delete(f'https://api.codemao.cn/web/forums/posts/' + str(post_id),
                          headers=headers).status_code != 204:
                return False

            return True
        except:
            return False
