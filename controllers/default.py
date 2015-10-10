# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    posts = db(db.post.id > 0).select();
    return dict(posts=posts)

@auth.requires_login()
def create():
    form = SQLFORM(db.post)
    if form.process().accepted:
        response.flash = 'Your blog was posted'
    return dict(form=form)

#@auth.requires_login()
def show():
    #TODO: Allow editing/ deletion if you're the user who created this
    cur_user = auth.user
    post = db.post(request.args(0,cast=int)) or redirect(URL('index'))
    title=post.title
    user_id=post.user_id
    username = db
    same = False;
    if auth.user:
    	same = cur_user.id == user_id
    body = post.body
    comments = db(db.post_com.post_id==post.id).select()
    user_id = request.args(0, cast=int)
    user = db(db.auth_user.id == user_id).select().first()
    username = user.first_name + " " + user.last_name
    #TODO: autofill db.comment.post_id with post.id
    
    db.post_com.post_id.default = post.id
    form = SQLFORM(db.post_com)
    if form.process().accepted:
        response.flash = 'Comment posted'
    return dict(same=same, title=title, post_id=post.id, username=username, user_id=user_id, body=body, comments=comments, form=form)

def profile():
    user_id = request.args(0, cast=int)
    user = db(db.auth_user.id == user_id).select().first()
    username = user.first_name + " " + user.last_name
    posts = db(db.post.user_id == user_id).select()
    return dict(user=user,username=username, posts=posts)

#Require specific user
#this crashes for some reason I have no fucking clue why
@auth.requires_login()
def edit():
    post_id = request.args(0,cast=int)
    record = db((db.post.id == post_id) &
		(db.post.user_id == auth.user.id)
		).select().first()
    form = SQLFORM(db.post,record).process()
    if form.accepted:
        session.flash = T('done!')
    return dict(form=form)

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
