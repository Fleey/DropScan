import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import {BrowserRouter, Link, Route, Switch} from 'react-router-dom';
import './index.css';
import TaskIndex from './view/Task/Index'
import Index from './view/Index';
import NotFound from './view/NotFound';
import * as serviceWorker from './serviceWorker';


import {Layout, Menu} from 'antd';
import Common from './Common';

const {Header, Footer} = Layout;

let getNowYear = () => {
    return new Date().getFullYear();
};

class RoutePage extends Component {

    private defaultSelectKeys = (props: any) => {
        let location = props.location.pathname;
        location = location.toLowerCase();
        if (Common.startWith('/task', location))
            return 'task';
        if (Common.startWith('/plugins', location))
            return 'plugins';
        if (Common.startWith('/user', location))
            return 'user';
        if(Common.startWith('/login',location) || Common.startWith('/register',location))
            return '';
        if (Common.startWith('/', location))
            return 'index';
        return '';
    };

    render() {
        return (
            <Layout className={"content"}>
                <Header className="header">
                    <div className="logo"/>
                    <Menu
                        theme="dark"
                        mode="horizontal"
                        defaultSelectedKeys={[this.defaultSelectKeys(this.props)]}
                        style={{lineHeight: '64px'}}
                    >
                        <Menu.Item key="index"><Link to={"/"}>首页</Link></Menu.Item>
                        <Menu.Item key="user"><Link to={"/User"}>用户中心</Link></Menu.Item>
                        <Menu.Item key="task"><Link to={"/Task"}>任务中心</Link></Menu.Item>
                        <Menu.Item key="plugins"><Link to={"/Plugins"}>插件广场</Link></Menu.Item>
                    </Menu>
                </Header>
                <Switch>
                    <Route path="/" exact component={Index}/>
                    <Route path="/Task" component={TaskIndex}/>
                    <Route component={NotFound}/>
                </Switch>
                <Footer style={{textAlign: 'center'}}>DorpScan ©{getNowYear()} Created by Fleey</Footer>
            </Layout>
        );
    }
}

ReactDOM.render(
    <BrowserRouter>
        <Route path="/" component={RoutePage}/>
    </BrowserRouter>
    , document.getElementById('body'));
serviceWorker.unregister();

