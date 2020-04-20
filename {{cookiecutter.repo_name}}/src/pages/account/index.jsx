import React from 'react';
import loginRequired from 'util/loginRequired';
import { Form, Field, Formik } from 'formik';
import {
    updateUser,
    ProfileSchema,
    useCurrentUser,
    useMutateCurrentUser,
    useIsAuthenticated,
} from 'models/user';

import Link from 'components/router/Link';
import Typography from '@material-ui/core/Typography';
import Button from '@material-ui/core/Button';
import { TextField, CheckboxWithLabel } from 'formik-material-ui';
import Container from '@material-ui/core/Container';
import { makeStyles } from '@material-ui/core/styles';
import Grid from '@material-ui/core/Grid';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';
import Avatar from '@material-ui/core/Avatar';
import FormControlLabel from '@material-ui/core/FormControlLabel';

import { useSnackbar } from 'notistack';

const useStyles = makeStyles(theme => ({
    paper: {
        display: 'flex',
        alignItems: 'center',
        flexDirection: 'column',
        paddingTop: theme.spacing(2),
        paddingBottom: theme.spacing(4),
    },
    grid: {
        marginBottom: theme.spacing(1),
    },
    bottomSpace: {
        marginBottom: theme.spacing(2),
    },
}));

const EditProfile = () => {
    const classes = useStyles();
    const { enqueueSnackbar, closeSnackbar } = useSnackbar();
    const me = useCurrentUser();
    const mutate = useMutateCurrentUser();
    return (
        <Container className={classes.paper} component="main" maxWidth="xs">
            <Avatar>
                <AccountCircleIcon />
            </Avatar>
            <Typography variant="h1" variant="h5">
                Update your profile
            </Typography>
            {me ? (
                <Formik
                    initialValues={{
                        first_name: me.first_name,
                        last_name: me.last_name,
                    }}
                    className={classes.form}
                    validateOnChange
                    validationSchema={ProfileSchema}
                    onSubmit={(values, actions) => {
                        mutate(updateUser(values), false)
                            .then(response => {
                                enqueueSnackbar('Successfully updated profile!', {
                                    variant: 'success',
                                });
                                return response;
                            })
                            .then(response => {
                                actions.setSubmitting(false);
                                return response;
                            })
                            .catch(error => {
                                actions.setSubmitting(false);
                                if (error.non_field_errors) {
                                    enqueueSnackbar(error.non_field_errors, {
                                        variant: 'error',
                                    });
                                } else {
                                    actions.setErrors(error);
                                }
                            });
                    }}
                >
                    <Form>
                        <Grid container spacing={2} className={classes.grid}>
                            <Grid item xs={12} sm={6}>
                                <Field
                                    component={TextField}
                                    name="first_name"
                                    label="First Name"
                                    placeholder="Enter First Name"
                                />
                            </Grid>

                            <Grid item xs={12} sm={6}>
                                <Field
                                    name="last_name"
                                    component={TextField}
                                    label="Last Name"
                                    placeholder="Enter Last Name"
                                />
                            </Grid>
                        </Grid>
                        <Button
                            fullWidth
                            variant="outlined"
                            type="submit"
                            className={classes.bottomSpace}
                        >
                            Update profile
                        </Button>
                    </Form>
                </Formik>
            ) : (
                <div>Loading</div>
            )}
        </Container>
    );
};

EditProfile.getInitialProps = async ctx => {
    console.log('a bunch ofp age specific stuff I want to do');
    return { foo: 'bar' };
};

EditProfile.getInitialProps = loginRequired(EditProfile.getInitialProps);

export default EditProfile;
