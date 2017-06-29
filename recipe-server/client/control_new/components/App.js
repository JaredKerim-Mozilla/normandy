import { Layout, LocaleProvider } from 'antd';
import enUS from 'antd/lib/locale-provider/en_US';
import PropTypes from 'prop-types';
import React from 'react';

import NavigationCrumbs from 'control_new/components/common/NavigationCrumbs';

const { Content, Header, Sider } = Layout;

export default function App({ children }) {
  return (
    <LocaleProvider locale={enUS}>
      <Layout>
        <Header>
          <div className="logo">
            SHIELD Control Panel
          </div>
        </Header>

        <Layout>
          <Sider width={200} className="sidebar">
            Menu goes here.
          </Sider>

          <Layout className="content-wrapper">
            <NavigationCrumbs />

            <Content className="content">
              {children}
            </Content>
          </Layout>
        </Layout>
      </Layout>
    </LocaleProvider>
  );
}

App.propTypes = {
  children: PropTypes.any,
};