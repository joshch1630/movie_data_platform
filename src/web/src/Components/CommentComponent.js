import React, { useState, useEffect } from 'react';
import DataService from '../Service/DataApiService';
import Box from '@mui/material/Box';
import Card from '@mui/material/Card';
import CardContent from '@mui/material/CardContent';
import Typography from '@mui/material/Typography';
import Paper from '@mui/material/Paper';
import Grid from '@mui/material/Grid';
import TextField from '@mui/material/TextField';
import LoadingButton from '@mui/lab/LoadingButton';
import Stack from '@mui/material/Stack';
import LinearProgress from '@mui/material/LinearProgress';
import { useForm } from 'react-hook-form';
import { yupResolver } from '@hookform/resolvers/yup';
import * as Yup from 'yup';
import Snackbar from '@mui/material/Snackbar';
import MuiAlert from '@mui/material/Alert';

const Alert = React.forwardRef(function Alert(props, ref) {
    return <MuiAlert elevation={6} ref={ref} variant="filled" {...props} />;
});

const CommentComponent = (props) => {

    const [comments, setComments] = useState([]);
    const [isLoaded, setIsLoaded] = useState(false);
    const [isLoadingSubmit, setIsLoadingSubmit] = useState(false);
    const [successAlertOpen, setSuccessAlertOpen] = useState(false);
    const [errorAlertOpen, setErrorAlertOpen] = useState(false);

    useEffect(() => {
        getComments(props.sectionId);
    }, [props.sectionId]);

    async function getComments(sectionId) {
        try {
            let result = await DataService.getCommentsApi(sectionId);
            setComments(result);
            setIsLoaded(true);
        } catch (err) {
            console.log(err)
        }
    }

    const validationSchema = Yup.object().shape({
        name: Yup.string()
            .required('Name is required')
            .max(20, 'Name must not exceed 20 characters'),
        content: Yup.string()
            .required('Content is required')
            .max(1500, 'Content must not exceed 1500 characters')
    });

    const { register, handleSubmit, formState: { errors }, reset } = useForm({
        resolver: yupResolver(validationSchema)
    });

    const onSubmit = data => {
        postComment(data)
    };

    async function postComment(comment) {
        setIsLoadingSubmit(true);

        comment["sectionId"] = props.sectionId;

        try {
            await DataService.postCommentApi(comment);
            reset({
                name: "",
                content: ""
            });
            setIsLoadingSubmit(false);
            setSuccessAlertOpen(true);
        } catch (err) {
            console.log(err)
            setErrorAlertOpen(true);
        }
    };

    const handleClose = (event, reason) => {
        if (reason === 'clickaway') {
            return;
        }
        setSuccessAlertOpen(false);
        setErrorAlertOpen(false);
    };

    return (
        <Box>
            <Box className='header'>
                <Stack direction="row" spacing={2}>
                    <img src="https://img.icons8.com/ios-filled/30/000000/comments.png" alt="Comment" />
                    <h3 className='title'>Comment</h3>
                </Stack>
            </Box>

            <Box>
                <Paper>
                    <Box px={3} py={2}>
                        <Grid container spacing={1}>
                            <Grid item xs={12} md={6} lg={3}>
                                <TextField required id="name" name="name" label="Name"
                                    fullWidth margin="dense"  {...register('name')}
                                    error={errors.name ? true : false} />
                                <Typography variant="inherit" color="textSecondary">
                                    {errors.name?.message}
                                </Typography>
                            </Grid>
                            <Grid item xs={12} >
                                <TextField required id="content" name="content" label="Content"
                                    fullWidth multiline rows={5} margin="dense" {...register('content')}
                                    error={errors.content ? true : false} />
                                <Typography variant="inherit" color="textSecondary">
                                    {errors.content?.message}
                                </Typography>
                            </Grid>
                        </Grid>

                        <Box mt={2}>
                            <LoadingButton variant="contained" color="primary"
                                onClick={handleSubmit(onSubmit)}
                                loading={isLoadingSubmit}
                                loadingIndicator="Loading...">
                                Submit
                            </LoadingButton>
                        </Box>
                    </Box>
                    <Snackbar open={successAlertOpen} autoHideDuration={6000} onClose={handleClose}>
                        <Alert onClose={handleClose} severity="success" sx={{ width: '100%' }}>
                            Submit Successfully!
                        </Alert>
                    </Snackbar>
                    <Snackbar open={errorAlertOpen} autoHideDuration={6000} onClose={handleClose}>
                        <Alert onClose={handleClose} severity="error" sx={{ width: '100%' }}>
                            Oops, something went wrong! Please try again later.
                        </Alert>
                    </Snackbar>
                </Paper>
            </Box>

            <Box>
                <h2 >{isLoaded ? null : <LinearProgress />}</h2>
                {comments.map(comment => (
                    <Card key={comment.commentId} sx={{ mt: 2 }}>
                        <CardContent>
                            <Stack direction="row" spacing={2}>
                                <Typography color="text.secondary" gutterBottom>
                                    {comment.name}
                                </Typography>
                                <Typography color="text.secondary" gutterBottom>
                                    • {comment.createDate} (UTC)
                                </Typography>
                            </Stack>
                            <Typography sx={{ whiteSpace: 'pre-line' }}>
                                {comment.content}
                            </Typography>
                        </CardContent>
                    </Card>
                ))}
            </Box>
        </Box>
    );
}

export default CommentComponent;