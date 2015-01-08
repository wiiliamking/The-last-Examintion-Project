Time scheduler

功能：制定每周日程表，记录任务完成状态并发布分享

后台数据结构

class user{
    name
    password 
    // 不解释。。。
    schedule[]  
    // 日程表数组，一周一个元素，每一周为一个schedule类，作为历史记录
    proto 
    //schedule类，为目前使用的日程安排
    slogan 
    //口号
}

class schedule {
    content[] 
    // 日程内容，以课程表形式一格一格划分，每格有固定时间段（方便处理。。。。），用一维模拟二维，每一个为一个event类
    specification 
    // 日程说明
    setUpTime 
    // 建立时间，proto则为修改时间
}

class event {
    summary 
    //  任务概述
    specifiction 
    // 详细说明
    completed 
    // 是否完成,值为1或0
    feeling 
    //  感想
    photo 
    // 照片证明
    comments[] 
    //其它人的评论
}

class comment {
    content
    //内容
    name
    //留言者
}

页面内容

index.html 
//主页，显示当天的日程（每一格只显示概述，点击格弹出小框显示详细说明）, 前端接收数据： year, month, day（当天日期）, schedule(当天日程，只有当天的事件，非全部，就是一维的数组)

login.html
//登录页面，交互数据：name, password，使用AJAX提交用户名密码，以使用户名密码错误时页面不跳转而只是弹出错误警示框。

editor.html
//编辑页面，显示proto的日程内容，点击对应格弹出一个表单框输入修改内容。前端接收数据: user对象

share.html
//用户日程展示，分享用户的日程完成情况，该页只列出用户的列表。前端接收数据: user列表（只含name和slogan成员)，点击列表进入用户历史日程分享

sharedetail.html
//用户日程分享详细，点击不同周显示不同周的日程完成情况，显示与编辑页面相似，但点击小格显示的内容多出了完成情况、感想、照片和评论。前端接收数据，特定user对象

arranger.html
//针对空闲时间不知道如何安排的用户所设，输入自己最近要完成的任务及dealine，让系统来安排日程，前端接收数据:无

confirm.html
//显示系统生成的日程表，让用户判断是否采用。前端接收数据: schedule对象

前端get请求:

/index
/login
/editor
/share
/share/:name //对应sharedetial.html:
/arranger
/confirm

//此类请求直接渲染对应模板，有些请求包含后端用户认证

前端post请求:

/login 
//post数据有name、password，使用ajax发送，以便用户名密码错误时弹出错误警示框而不跳转页面，响应数据为错误信息或success信息。
/editor 
//post数据为修改格的坐标row, col和修改后的summary和specification，相应信息为success
/arranger 
//post数据为事件列表eventList，每个事件对象包含成员summary, specification, deadline(成员year,month,day)，及所需时间time(hour为单位)
/confirm 
//post数据为待确认的schedule对象

===========================
