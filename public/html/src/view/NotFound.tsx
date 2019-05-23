import React, {Component} from 'react';
import {Empty, Layout} from 'antd';

const {Content} = Layout;

class NotFound extends Component {
    render() {
        return (
            <Content style={{padding: '0 50px', marginTop: '10%'}}>
                <Empty description={
                    <div>
                        <p>404 Not Found</p>
                        <p>页面丢失或正在施工中</p>
                    </div>
                }/>
            </Content>
        );
    }
}

export default NotFound