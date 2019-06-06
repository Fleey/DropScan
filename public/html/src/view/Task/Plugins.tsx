import React, {Component} from 'react';
import {Button, Icon, Tooltip, Tag} from "antd";

const ButtonGroup = Button.Group;

class Plugins extends Component {
    render() {
        return (
            <div>
                <div className="tootls">

                </div>
                <div className="card">
                    <div className="body">
                        <div className="left" style={{float: "left", fontSize: 30, paddingRight: 16}}>
                            <Tooltip placement="topLeft" title="待审核" arrowPointAtCenter>
                                <Icon type="experiment"/>
                            </Tooltip>
                        </div>
                        <div className="content" style={{float: "left", width: "calc(100% - 200px)"}}>
                            <div className="title" style={{
                                marginBottom: 8,
                                color: "rgba(0, 0, 0, 0.85)",
                                fontSize: 16,
                                fontWeight: 500
                            }}><Tag color="#108ee9">私有</Tag>CVE-20190807
                            </div>
                            <div className="desc" style={{color: "rgba(0, 0, 0, 0.45)"}}>
                                WordPress 4.7.0/4.7.1 REST API 内容注入漏洞
                            </div>
                        </div>
                        <div className="right" style={{float: "right", fontSize: 30, paddingLeft: 16}}>
                            <ButtonGroup>
                                <Tooltip placement="topLeft" title="删除插件" arrowPointAtCenter>
                                    <Button><Icon type="rest"/></Button>
                                </Tooltip>
                            </ButtonGroup>
                        </div>
                        <div style={{clear: "both"}}/>
                    </div>
                </div>
                <div className="card">
                    <div className="body">
                        <div className="left" style={{float: "left", fontSize: 30, paddingRight: 16}}>
                            <Tooltip placement="topLeft" title="已审核通过" arrowPointAtCenter>
                                <Icon type="experiment" style={{color: "#87d068"}}/>
                            </Tooltip>
                        </div>
                        <div className="content" style={{float: "left", width: "calc(100% - 200px)"}}>
                            <div className="title" style={{
                                marginBottom: 8,
                                color: "rgba(0, 0, 0, 0.85)",
                                fontSize: 16,
                                fontWeight: 500
                            }}><Tag color="#108ee9">公开</Tag>CVE-20190807
                            </div>
                            <div className="desc" style={{color: "rgba(0, 0, 0, 0.45)"}}>
                                WordPress 4.7.0/4.7.1 REST API 内容注入漏洞
                            </div>
                        </div>
                        <div className="right" style={{float: "right", fontSize: 30, paddingLeft: 16}}>
                            <ButtonGroup>
                                <Tooltip placement="topLeft" title="删除插件" arrowPointAtCenter>
                                    <Button><Icon type="rest"/></Button>
                                </Tooltip>
                            </ButtonGroup>
                        </div>
                        <div style={{clear: "both"}}/>
                    </div>
                </div>
            </div>
        );
    }
}

export default Plugins