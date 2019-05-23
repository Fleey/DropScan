import React, {Component} from 'react';
import {Layout, Menu, Breadcrumb, Icon} from 'antd';
import {Route, Switch} from "react-router";
import {Link} from "react-router-dom";

import TaskList from "./TaskList";
import MachineList from "./MachineList";
import PrivatePlugins from "./PrivatePlugins";
import Common from "../../Common";

const {Content, Sider} = Layout;


class Index extends Component {

    private defaultCrumbName = (props: any) => {
        let location = props.location.pathname;
        location = location.toLowerCase();
        if (Common.startWith('/task/taskList', location))
            return '任务列表';
        if (Common.startWith('/task/machinelist', location))
            return '机器列表';
        if (Common.startWith('/task/privateplugins', location))
            return '私有插件';
        if (Common.startWith('/', location))
            return '任务列表';
        return '';
    };

    private defaultSelectKeyName = (props: any) => {
        let location = props.location.pathname;
        location = location.toLowerCase();
        if (Common.startWith('/task/taskList', location))
            return 'taskList';
        if (Common.startWith('/task/machinelist', location))
            return 'machineList';
        if (Common.startWith('/task/privateplugins', location))
            return 'privatePlugins';
        if (Common.startWith('/', location))
            return 'taskList';
        return '';
    };

    render() {
        return (
            <Content style={{padding: '0 50px'}}>
                <Breadcrumb style={{margin: '16px 0'}}>
                    <Breadcrumb.Item>首页</Breadcrumb.Item>
                    <Breadcrumb.Item>任务中心</Breadcrumb.Item>
                    <Breadcrumb.Item>{[this.defaultCrumbName(this.props)]}</Breadcrumb.Item>
                </Breadcrumb>
                <Layout style={{padding: '24px 0', background: '#fff'}}>
                    <Sider width={200} style={{background: '#fff', minHeight: '100%'}}>
                        <Menu
                            mode="inline"
                            defaultSelectedKeys={[this.defaultSelectKeyName(this.props)]}
                            defaultOpenKeys={['sub1']}
                            style={{height: '100%'}}
                        >
                            <Menu.Item key="taskList"><Link to={"/Task/TaskList"}><Icon
                                type="appstore"/>任务列表</Link></Menu.Item>
                            <Menu.Item key="machineList"><Link to={"/Task/MachineList"}><Icon type="ordered-list"/>机器列表</Link></Menu.Item>
                            <Menu.Item key="privatePlugins"><Link to={"/Task/PrivatePlugins"}><Icon type="database"/>私有插件</Link></Menu.Item>
                        </Menu>
                    </Sider>
                    <Content style={{padding: '0 24px', minHeight: 380}}>
                        <Switch>
                            <Route path="/Task/TaskList" component={TaskList}/>
                            <Route path="/Task/MachineList" component={MachineList}/>
                            <Route path="/Task/PrivatePlugins" component={PrivatePlugins}/>
                            <Route path="/Task/" component={TaskList}/>
                        </Switch>
                    </Content>
                </Layout>
            </Content>
        )
    }
}

export default Index