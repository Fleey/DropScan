<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>登录账户 | DorpScan - 智能扫描平台</title>
    <meta name="description" content="Responsive, Bootstrap, BS4">
    <meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1">
    <link rel="stylesheet" href="https://cdn.staticfile.org/animate.css/3.7.2/animate.min.css">
    <link rel="stylesheet" href="/static/css/site.min.css">
</head>
<body class="layout-row">
<div class="flex" id="content">
    <div class="w-xl w-auto-sm mx-auto py-5">
        <div class="p-4 d-flex flex-column h-100">
            <a href="/" class="navbar-brand align-self-center">
                <i style="width: 24px;height: 24px;" data-feather="compass"></i>
                <span class="hidden-folded d-inline l-s-n-1x align-self-center">DorpScan</span>
            </a>
        </div>
        <div class="card">
            <div id="content-body" >
                <div class="p-3 p-md-5"><h5>欢迎使用 DorpScan</h5>
                    <p>
                        <small class="text-muted">登录账户进行使用高级功能</small>
                    </p>
                    <form class="" role="form" action="dashboard.html">
                        <div class="form-group">
                            <label>账户</label>
                            <input type="text" id="account" class="form-control" placeholder="邮箱账户/用户名称">
                        </div>
                        <div class="form-group">
                            <label>密码</label>
                            <input type="password" id="password" class="form-control" placeholder="密码"/>
                            <div class="my-3 text-right"><a href="/ForgotPassword" class="text-muted">忘记密码?</a></div>
                        </div>
                        <div class="checkbox mb-3">
                            <label class="ui-check">
                                <input type="checkbox"><i></i>记住账户
                            </label>
                        </div>
                        <button type="button" class="btn btn-primary mb-4" id="login">登录</button>
                        <div>还没有账户? <a href="/SignUp" class="text-primary" data-pjax>注册</a></div>
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

            })
        }
    });
</script>
</body>
</html>