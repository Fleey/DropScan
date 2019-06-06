import React, {Component} from 'react';
import {Form, Icon, Input, Button, Checkbox} from 'antd';

import '../css/Login.css';
import {Link} from 'react-router-dom';

class NormalLoginForm extends React.Component {
    handleSubmit = (e: any) => {
        e.preventDefault();
        // @ts-ignore
        this.props.form.validateFields((err: any, values: any) => {
            if (!err) {
                console.log('Received values of form: ', values);
            }
        });
    };

    render() {
        // @ts-ignore
        const {getFieldDecorator} = this.props.form;
        return (
            <Form onSubmit={this.handleSubmit} className="login-form">
                <h1 className={"title"}>DorpHelp</h1>
                <Form.Item>
                    {getFieldDecorator('username', {
                        rules: [{required: true, message: '必须输入用户名称!'}],
                    })(
                        <Input
                            prefix={<Icon type="user" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            placeholder="用户名"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('password', {
                        rules: [{required: true, message: '必须输入用户密码!'}],
                    })(
                        <Input
                            prefix={<Icon type="lock" style={{color: 'rgba(0,0,0,.25)'}}/>}
                            type="password"
                            placeholder="密码"
                        />,
                    )}
                </Form.Item>
                <Form.Item>
                    {getFieldDecorator('remember', {
                        valuePropName: 'checked',
                        initialValue: true,
                    })(<Checkbox>记住账号</Checkbox>)}
                    <Link to={"/FindPassword"} className={"login-form-forgot"}>找回密码</Link>
                    <Button type="primary" htmlType="submit" className="login-form-button">
                        登录账号
                    </Button>
                    或 <Link to={"/Register"}>注册账号</Link>
                </Form.Item>
            </Form>
        );
    }
}

const WrappedNormalLoginForm = Form.create({name: 'normal_login'})(NormalLoginForm);

class Login extends Component {
    render() {
        return (<div id={"login-div"}>
            <WrappedNormalLoginForm/>
        </div>);
    }
}

export default Login