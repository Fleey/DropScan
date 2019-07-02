<?php

namespace app\user\controller;

use think\Controller;

class Template extends Controller
{
    public function viewSignIn()
    {
        return $this->fetch('/SignInTemplate');
    }
    public function viewSignUp()
    {
        return $this->fetch('/SignUpTemplate');
    }

}