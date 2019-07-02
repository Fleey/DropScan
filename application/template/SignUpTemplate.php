<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>注册账户 | DorpScan - 智能扫描平台</title>
    <meta name="description" content="Responsive, Bootstrap, BS4">
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
    <link rel="stylesheet" href="https://cdn.staticfile.org/animate.css/3.7.2/animate.min.css">
    <link rel="stylesheet" href="/static/css/site.min.css">
</head>
<body class="layout-row" id="body">
<div class="flex" id="content">
    <div class="w-xl w-auto-sm mx-auto py-5">
        <div class="p-4 d-flex flex-column h-100">
            <a href="/" class="navbar-brand align-self-center">
                <i style="width: 24px;height: 24px;" data-feather="compass"></i>
                <span class="hidden-folded d-inline l-s-n-1x align-self-center">DorpScan</span>
            </a>
        </div>
        <div class="card">
            <div id="content-body">
                <div class="p-3 p-md-5"><h5>欢迎使用 DorpScan</h5>
                    <p>
                        <small class="text-muted">注册账户进行使用高级功能</small>
                    </p>
                    <form class="" role="form">
                        <div class="form-group">
                            <label>用户名称</label>
                            <input type="text" id="username" class="form-control" placeholder="用户名称">
                        </div>
                        <div class="form-group">
                            <label>邮箱账户</label>
                            <input type="email" id="email" class="form-control" placeholder="邮箱账号">
                        </div>
                        <div class="form-group">
                            <label>密码</label>
                            <input type="password" id="password" class="form-control" placeholder="密码"/>
                        </div>
                        <div id="signUpCode"></div>
                        <button type="button" class="btn btn-primary mb-4" id="register">注册</button>
                        <div>已经有账号? <a href="/SignIn" class="text-primary">登录</a></div>
                    </form>
                </div>
            </div>
        </div>
        <div class="text-center text-muted">&copy; Copyright. DorpScan</div>
    </div>
</div>
<script src="https://cdn.staticfile.org/jquery/3.4.1/jquery.min.js"></script>
<script src="https://cdn.staticfile.org/jquery.pjax/2.0.1/jquery.pjax.min.js"></script>
<script src="https://cdn.staticfile.org/feather-icons/4.21.0/feather.min.js"></script>
<script src="/static/js/gt.js"></script>
<script>
    $(function ($) {
        feather.replace();
        if($.support.pjax){
            $(document).pjax('a[target!=_blank]', '.card>#content-body>div', {fragment:'.card>#content-body>div', timeout:8000});
            $(document).on('pjax:send', function() {
                $('.card').addClass('js-Pjax-onswitch');
                $('.card>#content-body>div').addClass('fadeOutRight animated fast');
            });
            $(document).on('pjax:complete', function() {
                setTimeout(function () {
                    $('.card>#content-body>div').removeClass('fadeOutRight').addClass('fadeInLeft');
                    setTimeout(function () {
                        $('.card>#content-body>div').removeClass('fadeInLeft fast animated');
                        $('.card').removeClass('js-Pjax-onswitch');
                    },800);
                },200)
            });
            $(document).on('ready pjax:end', function(event) {
                // $(event.target).initializeMyPlugin()
            })
        }
        loadRegisterGT();
        console.log('加载了')
    });
    function loadRegisterGT(){
        var handlerEmbed = function (captchaObj) {
            $("#register").click(function (e) {
                var validate = captchaObj.getValidate();
                if (!validate) {
                    swal('必须要验证人机身份，您需要按照提示点击下方验证码', {
                        buttons: false,
                        timer: 1500,
                        icon: 'info'
                    });
                    e.preventDefault();
                    return true;
                }
                var uid = $('#uid').val();
                var password = $('#password').val();
                if (uid.length === 0) {
                    swal('商户ID不能为空', {
                        buttons: false,
                        timer: 1500,
                        icon: 'info'
                    });
                    return true;
                }
                if (password.length === 0) {
                    swal('商户密码不能为空', {
                        buttons: false,
                        timer: 1500,
                        icon: 'info'
                    });
                    return true;
                }
                $.post(baseUrl + 'auth/user/Login', {
                    uid: uid,
                    password: password,
                    geetest_validate: $('input[name="geetest_validate"]').val(),
                    geetest_seccode: $('input[name="geetest_seccode"]').val(),
                    geetest_challenge: $('input[name="geetest_challenge"]').val()
                }, function (data) {
                    if (data['status'] === 0) {
                        swal(data['msg'], {
                            buttons: false,
                            timer: 1500,
                            icon: 'warning'
                        });
                        return true;
                    }
                    if (data['status'] === -1) {
                        swal(data['msg'], {
                            buttons: false,
                            timer: 1500,
                            icon: 'warning'
                        });
                        captchaObj.reset();
                        return true;
                    }
                    swal('登陆成功，将为您转跳页面', {
                        buttons: false,
                        timer: 1500,
                        icon: 'success'
                    });
                    setTimeout(function () {
                        window.location.href = baseUrl + 'user/Index';
                    }, 1500);
                });
            });
            $('#signUpCode').css({'padding-bottom': '1rem'});
            captchaObj.appendTo('#signUpCode');
            setTimeout(function () {
                $('.geetest_holder.geetest_wind').css({
                    minWidth: '100%'
                });
            },100);
        };
        $.ajax({
            url: "/auth/user/GeetestInfo?t=" + (new Date()).getTime(), // 加随机数防止缓存
            type: "get",
            dataType: "json",
            success: function (data) {
                initGeetest({
                    gt: data.gt,
                    challenge: data.challenge,
                    new_captcha: data.new_captcha,
                    product: "embed",
                    offline: !data.success,
                    width: '100%'
                }, handlerEmbed);
            }
        });
    }
</script>
</body>
</html>