import React, {Component} from 'react';
import '../css/Index.css'
import {Button, Layout} from "antd";
import {Link} from "react-router-dom";

const {Content} = Layout;

class Index extends Component {
    state = {};

    render() {
        return (
            <Content style={{padding: '0 50px'}}>
                <div className="panel">
                    <p className="title">DorpScan</p>
                    <p className="desc">分布式网站信息扫描平台</p>
                    <div className={"button-group"} style={{marginTop: "2rem"}}>
                        <Link to="/Login">
                            <Button type="primary" style={{width: "128px", height: "36px", marginRight: "22px"}}>登录</Button>
                        </Link>
                        <Link to="/Register">
                            <Button style={{width: "128px", height: "36px"}}>注册</Button>
                        </Link>
                    </div>
                </div>
            </Content>
        )
    }
}

export default Index