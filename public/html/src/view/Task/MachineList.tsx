import React, {Component} from 'react';
import {BackTop, Button, Icon, Progress, Tooltip} from "antd";

const ButtonGroup = Button.Group;

class MachineList extends Component {
    render() {
        return (
            <div>
                <BackTop/>
                <div className="card">
                    <div className="body">
                        <div className="left" style={{float: "left", fontSize: 30, paddingRight: 16}}>
                            <Icon type="desktop"/>
                        </div>
                        <div className="content" style={{float: "left", width: "calc(100% - 200px)"}}>
                            <div className="title" style={{
                                marginBottom: 8,
                                color: "rgba(0, 0, 0, 0.85)",
                                fontSize: 16,
                                fontWeight: 500
                            }}>127.0.0.1
                            </div>
                            <div className="desc" style={{color: "rgba(0, 0, 0, 0.45)"}}>
                                Windows-10-10.0.17763-SP0 AMD64（00:1a:7d:da:71:13）
                            </div>
                        </div>
                        <div className="right" style={{float: "right", fontSize: 30, paddingLeft: 16}}>
                            <ButtonGroup>
                                <Tooltip placement="topLeft" title="注销机器" arrowPointAtCenter>
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
                            <Icon type="desktop" style={{color: "#7ebc59"}}/>
                        </div>
                        <div className="content" style={{float: "left", width: "calc(100% - 200px)"}}>
                            <div className="title" style={{
                                marginBottom: 8,
                                color: "rgba(0, 0, 0, 0.85)",
                                fontSize: 16,
                                fontWeight: 500
                            }}>127.0.0.2
                            </div>
                            <div className="desc" style={{color: "rgba(0, 0, 0, 0.45)"}}>
                                Linux-10-10.0.17763-SP0 AMD64（00:1a:7d:da:71:13）
                            </div>
                        </div>
                        <div className="right" style={{float: "right", fontSize: 30, paddingLeft: 16}}>
                            <ButtonGroup>
                                <Tooltip placement="topLeft" title="注销机器" arrowPointAtCenter>
                                    <Button><Icon type="poweroff"/></Button>
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

export default MachineList