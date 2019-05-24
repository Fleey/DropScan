import React, {Component} from 'react';
import {BackTop, Icon, Row, Col, Button, Tooltip, Progress, Divider, Drawer, Tag, Switch} from "antd";
import '../../css/task/TaskList.css'

const ButtonGroup = Button.Group;

const DescriptionItem = (props: { title: any, content: any }) => (
    <div className="a1">
        <p className="a2">
            {props.title}:
        </p>
        {props.content}
    </div>
);

const DrawTaskStatusDiv = (props: { status: any }) => {
    console.log(props);
    return (<p>233</p>)
};


class TaskList extends Component {

    private defaultLoadingMsg = '加载中...';

    private defaultTaskInfo = {
        visible: false,
        isScanC: false,
        target: this.defaultLoadingMsg,
        createTime: this.defaultLoadingMsg,
        endTime: this.defaultLoadingMsg,
        userAgent: this.defaultLoadingMsg,
        cookie: this.defaultLoadingMsg,
        dnsList: this.defaultLoadingMsg,
        nmapArgs: this.defaultLoadingMsg,
        pluginThreadNum: 0,
        pluginTotalNum: 0,
        status: 0,
        proxy: {
            isOpen: false,
            host: this.defaultLoadingMsg,
            port: 0,
            type: this.defaultLoadingMsg
        }
    };


    state = {
        taskInfo: this.defaultTaskInfo
    };

    showDrawer = () => {
        this.state.taskInfo.visible = true;
        this.setState(this.state);
    };

    closeDrawer = () => {
        this.state.taskInfo.visible = false;
        this.setState(this.state);
    };

    render() {
        return <div>
            <BackTop/>
            <div className="card">
                <div className="body">
                    <div className="left" style={{float: "left", fontSize: 30, paddingRight: 16}}>
                        <Icon type="close" style={{color: "#f5222d"}}/>
                    </div>
                    <div className="content" style={{float: "left", width: "calc(100% - 200px)"}}>
                        <div className="title" style={{
                            marginBottom: 8,
                            color: "rgba(0, 0, 0, 0.85)",
                            fontSize: 16,
                            fontWeight: 500
                        }}>blog.fleey.cn
                        </div>
                        <div className="desc" style={{color: "rgba(0, 0, 0, 0.45)"}}>
                            <Progress percent={64} status="exception"/>
                        </div>
                    </div>
                    <div className="right" style={{float: "right", fontSize: 30, paddingLeft: 16}}>
                        <ButtonGroup>
                            <Tooltip placement="topLeft" title="查看信息" arrowPointAtCenter>
                                <Button onClick={this.showDrawer}><Icon type="search"/></Button>
                            </Tooltip>
                            <Tooltip placement="topLeft" title="终止任务" arrowPointAtCenter>
                                <Button><Icon type="poweroff"/></Button>
                            </Tooltip>
                        </ButtonGroup>
                    </div>
                    <div style={{clear: "both"}}/>
                </div>
            </div>
            <div className="card">
                <div className="body">
                    <div className="left" style={{float: "left", fontSize: 30, paddingRight: 16}}>
                        <Icon type="hourglass" style={{color: "#1890ff"}} theme="filled"/>
                    </div>
                    <div className="content" style={{float: "left", width: "calc(100% - 200px)"}}>
                        <div className="title" style={{
                            marginBottom: 8,
                            color: "rgba(0, 0, 0, 0.85)",
                            fontSize: 16,
                            fontWeight: 500
                        }}>blog.fleey.cn
                        </div>
                        <div className="desc" style={{color: "rgba(0, 0, 0, 0.45)"}}>
                            <Progress percent={16} status="active"/>
                        </div>
                    </div>
                    <div className="right" style={{float: "right", fontSize: 30, paddingLeft: 16}}>
                        <ButtonGroup>
                            <Tooltip placement="topLeft" title="查看信息" arrowPointAtCenter>
                                <Button><Icon type="search"/></Button>
                            </Tooltip>
                            <Tooltip placement="topLeft" title="终止任务" arrowPointAtCenter>
                                <Button><Icon type="poweroff"/></Button>
                            </Tooltip>
                        </ButtonGroup>
                    </div>
                    <div style={{clear: "both"}}/>
                </div>
            </div>
            <div className="card">
                <div className="body">
                    <div className="left" style={{float: "left", fontSize: 30, paddingRight: 16}}>
                        <Icon type="check" style={{color: "#52c41a"}}/>
                    </div>
                    <div className="content" style={{float: "left", width: "calc(100% - 200px)"}}>
                        <div className="title" style={{
                            marginBottom: 8,
                            color: "rgba(0, 0, 0, 0.85)",
                            fontSize: 16,
                            fontWeight: 500
                        }}>blog.fleey.cn
                        </div>
                        <div className="desc" style={{color: "rgba(0, 0, 0, 0.45)"}}>
                            <Progress percent={100}/>
                        </div>
                    </div>
                    <div className="right" style={{float: "right", fontSize: 30, paddingLeft: 16}}>
                        <ButtonGroup>
                            <Tooltip placement="topLeft" title="查看信息" arrowPointAtCenter>
                                <Button><Icon type="search"/></Button>
                            </Tooltip>
                            <Tooltip placement="topLeft" title="终止任务" arrowPointAtCenter>
                                <Button><Icon type="poweroff"/></Button>
                            </Tooltip>
                        </ButtonGroup>
                    </div>
                    <div className="clearFix"/>
                </div>
            </div>
            <Drawer
                width={640}
                placement="right"
                closable={false}
                onClose={this.closeDrawer}
                visible={this.state.taskInfo.visible}
            >
                <p className="a3">基本信息</p>
                <Row>
                    <Col span={12}>
                        <DescriptionItem title="任务当前状态" content={
                            <div>
                                <DrawTaskStatusDiv status={0}/>
                                <Tag color="#87d068"> 正在执行 </Tag>
                            </div>
                        }/>
                    </Col>
                    <Col span={12}>
                        <DescriptionItem title="是否扫描C段" content={
                            <Switch disabled={true}
                                    checkedChildren={<Icon type="check"/>}
                                    unCheckedChildren={<Icon type="close"/>}
                                    defaultChecked={this.state.taskInfo.isScanC}/>
                        }/>
                    </Col>
                    <Col span={12}>
                        <DescriptionItem title="创建时间" content={this.state.taskInfo.createTime}/>
                    </Col>
                    <Col span={12}>
                        <DescriptionItem title="完成时间" content={this.state.taskInfo.endTime}/>
                    </Col>
                    <Col span={12}>
                        <DescriptionItem title="线程速度" content={
                            <Tag>{this.state.taskInfo.pluginThreadNum}</Tag>
                        }/>
                    </Col>
                    <Col span={12}>
                        <DescriptionItem title="扫描插件数量" content={
                            <Tag>{this.state.taskInfo.pluginTotalNum}</Tag>
                        }/>
                    </Col>
                    <Col span={24}>
                        <DescriptionItem title="目标链接" content={this.state.taskInfo.target}/>
                    </Col>
                </Row>
                <Divider/>
                <p className="a3">详细信息</p>
                <Row>
                    <Col span={24}>
                        <DescriptionItem title="DNS List" content={this.state.taskInfo.dnsList}/>
                    </Col>
                    <Col span={24}>
                        <DescriptionItem title="Nmap Args" content={this.state.taskInfo.nmapArgs}/>
                    </Col>
                    <Col span={24}>
                        <DescriptionItem title="Cookie" content={this.state.taskInfo.cookie}/>
                    </Col>
                    <Col span={24}>
                        <DescriptionItem title="UserAgent" content={this.state.taskInfo.userAgent}/>
                    </Col>
                </Row>
                <Divider/>
                <p className="a3">代理转发</p>
                <Row>
                    {
                        this.state.taskInfo.proxy.isOpen ?
                            <div>
                                <Col span={24}>
                                    <DescriptionItem title="Proxy Type" content={this.state.taskInfo.proxy.type}/>
                                </Col>
                                <Col span={12}>
                                    <DescriptionItem title="Host" content={this.state.taskInfo.proxy.host}/>
                                </Col>
                                <Col span={12}>
                                    <DescriptionItem title="Port" content={this.state.taskInfo.proxy.port}/>
                                </Col>
                            </div>
                            :
                            <p>代理尚未启用</p>
                    }
                </Row>
            </Drawer>
        </div>;
    }
}

export default TaskList