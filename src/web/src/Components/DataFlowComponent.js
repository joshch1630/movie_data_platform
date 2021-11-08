import { useEffect } from 'react';
import ReactGA from 'react-ga';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import CardMedia from '@mui/material/CardMedia';
import CardContent from '@mui/material/CardContent';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dark } from 'react-syntax-highlighter/dist/esm/styles/prism';
// eslint-disable-next-line import/no-webpack-loader-syntax
import dataFlowReadMe from '!!raw-loader!../md/DATA_FLOW_README.md';

const DataFlowComponent = () => {

    useEffect(() => {
        if (process.env.NODE_ENV === 'production') {
            ReactGA.pageview('Data Flow page view');
        }
    }, []);

    return (
        <Box sx={{ flexGrow: 1, p: 2 }}>
            <Card>
                <CardMedia
                    component="img"
                    image="/img/data_flow.png"
                    alt="Data Flow" />
                <CardContent>
                    <ReactMarkdown
                        children={dataFlowReadMe}
                        remarkPlugins={[remarkGfm]}
                        components={{
                            code({ node, inline, className, children, ...props }) {
                                const match = /language-(\w+)/.exec(className || '')
                                return !inline && match ? (
                                    <SyntaxHighlighter
                                        children={String(children).replace(/\n$/, '')}
                                        style={dark}
                                        language={match[1]}
                                        PreTag="div"
                                        {...props}
                                    />
                                ) : (
                                    <code className={className} {...props}>
                                        {children}
                                    </code>
                                )
                            }
                        }}
                    />
                </CardContent>
            </Card>
        </Box>
    );
}

export default DataFlowComponent;