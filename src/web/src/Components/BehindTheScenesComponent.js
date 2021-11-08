import { useEffect } from 'react';
import ReactGA from 'react-ga';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import CardContent from '@mui/material/CardContent';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { dark } from 'react-syntax-highlighter/dist/esm/styles/prism';
// eslint-disable-next-line import/no-webpack-loader-syntax
import behindTheScenesReadMe from '!!raw-loader!../md/BEHIND_THE_SCENES_README.md';

const BehindTheScenesComponent = () => {

    useEffect(() => {
        if (process.env.NODE_ENV === 'production') {
            ReactGA.pageview('Behind The Scenes page view');
        }
    }, []);

    return (
        <Box sx={{ flexGrow: 1, p: 2 }}>
            <Card>
                <CardContent>
                    <ReactMarkdown
                        children={behindTheScenesReadMe}
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

export default BehindTheScenesComponent;