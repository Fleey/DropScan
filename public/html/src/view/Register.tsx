import React, {Component} from 'react';
import {
    Form,
    Input,
    Tooltip,
    Icon,
    Cascader,
    Select,
    Row,
    Col,
    Checkbox,
    Button,
    AutoComplete, Steps,
} from 'antd';

import "../css/Register.css"

const {Option} = Select;
const {Step} = Steps;

class RegistrationForm extends Component {
    state = {
        confirmDirty: false,
        autoCompleteResult: [],
        current: 0
    };

    handleSubmit = (e: any) => {
        e.preventDefault();
        // @ts-ignore
        this.props.form.validateFieldsAndScroll((err: any, values: any) => {
            if (!err) {
                console.log('Received values of form: ', values);
            }
        });
    };

    handleConfirmBlur = (e: any) => {
        const value = e.target.value;
        this.setState({confirmDirty: this.state.confirmDirty || !!value});
    };

    compareToFirstPassword = (rule: any, value: any, callback: any) => {
        // @ts-ignore
        const form = this.props.form;
        if (value && value !== form.getFieldValue('password')) {
            callback('两次密码不一致!');
        } else {
            callback();
        }
    };

    validateToNextPassword = (rule: any, value: any, callback: any) => {
        // @ts-ignore
        const form = this.props.form;
        if (value && this.state.confirmDirty) {
            form.validateFields(['confirm'], {force: true});
        }
        callback();
    };

    render() {
        // @ts-ignore
        const {getFieldDecorator} = this.props.form;

        const formItemLayout = {
            labelCol: {
                xs: {span: 24},
                sm: {span: 8},
            },
            wrapperCol: {
                xs: {span: 24},
                sm: {span: 16},
            },
        };
        const tailFormItemLayout = {
            wrapperCol: {
                xs: {
                    span: 24,
                    offset: 0,
                },
                sm: {
                    span: 16,
                    offset: 8,
                },
            },
        };
        const prefixSelector = getFieldDecorator('prefix', {
            initialValue: '86',
        })(
            <Select style={{width: 70}}>
                <Option value="86">+86</Option>
            </Select>,
        );

        return (
            <Form {...formItemLayout} onSubmit={this.handleSubmit}>
                <h1 className={"title"}>注册账户</h1>
                <div>
                    <div>
                        <Steps current={this.state.current}>
                            <Step title={this.state.current < 1 ? "正在操作" : "已完成"} description="验证手机号码"/>
                            <Step title={this.state.current < 2 ? "正在操作" : "已完成"} description="填写个人信息"/>
                            <Step title={this.state.current < 3 ? "正在操作" : "已完成"} description="完成注册"/>
                        </Steps>
                    </div>
                    <Button style={{ marginLeft: 8 }} onClick={() => {
                        this.state.current = this.state.current + 1;
                        this.setState(this.state);
                    }}>
                        Previous
                    </Button>
                </div>
            </Form>
        );
    }
}

const WrappedRegistrationForm = Form.create({name: 'register'})(RegistrationForm);


class Register extends Component {
    render() {
        return (
            <div className={"register"}>
                <WrappedRegistrationForm/>
            </div>
        );
    }
}

export default Register