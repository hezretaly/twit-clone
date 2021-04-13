--
-- PostgreSQL database dump
--

-- Dumped from database version 13.0
-- Dumped by pg_dump version 13.0

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: tcadmin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO tcadmin;

--
-- Name: followers; Type: TABLE; Schema: public; Owner: tcadmin
--

CREATE TABLE public.followers (
    follower_id integer,
    followed_id integer
);


ALTER TABLE public.followers OWNER TO tcadmin;

--
-- Name: post; Type: TABLE; Schema: public; Owner: tcadmin
--

CREATE TABLE public.post (
    id integer NOT NULL,
    body character varying(140),
    "timestamp" timestamp without time zone,
    user_id integer
);


ALTER TABLE public.post OWNER TO tcadmin;

--
-- Name: post_id_seq; Type: SEQUENCE; Schema: public; Owner: tcadmin
--

CREATE SEQUENCE public.post_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.post_id_seq OWNER TO tcadmin;

--
-- Name: post_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tcadmin
--

ALTER SEQUENCE public.post_id_seq OWNED BY public.post.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: tcadmin
--

CREATE TABLE public."user" (
    id integer NOT NULL,
    username character varying(64),
    email character varying(120),
    password_hash character varying(128),
    about_me character varying(140),
    last_seen timestamp without time zone,
    avatar_img character varying(64)
);


ALTER TABLE public."user" OWNER TO tcadmin;

--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: tcadmin
--

CREATE SEQUENCE public.user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.user_id_seq OWNER TO tcadmin;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: tcadmin
--

ALTER SEQUENCE public.user_id_seq OWNED BY public."user".id;


--
-- Name: post id; Type: DEFAULT; Schema: public; Owner: tcadmin
--

ALTER TABLE ONLY public.post ALTER COLUMN id SET DEFAULT nextval('public.post_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: tcadmin
--

ALTER TABLE ONLY public."user" ALTER COLUMN id SET DEFAULT nextval('public.user_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: tcadmin
--

COPY public.alembic_version (version_num) FROM stdin;
355af03a6325
\.


--
-- Data for Name: followers; Type: TABLE DATA; Schema: public; Owner: tcadmin
--

COPY public.followers (follower_id, followed_id) FROM stdin;
2	1
4	1
4	2
\.


--
-- Data for Name: post; Type: TABLE DATA; Schema: public; Owner: tcadmin
--

COPY public.post (id, body, "timestamp", user_id) FROM stdin;
1	Hi everyone I'm Susan	2021-04-13 11:13:39.994169	2
2	Well, that was my first post	2021-04-13 13:17:00.663537	2
3	And that was my second post.	2021-04-13 13:17:18.053257	2
4	Hello this is MY first post🤙	2021-04-13 13:19:31.662517	1
5	I am super exited to join this app	2021-04-13 16:38:05.274445	4
6	I look forward to use it more often and see what everyone else think about my opinions.	2021-04-13 16:39:27.934345	4
7	69	2021-04-13 16:39:44.525288	4
\.


--
-- Data for Name: user; Type: TABLE DATA; Schema: public; Owner: tcadmin
--

COPY public."user" (id, username, email, password_hash, about_me, last_seen, avatar_img) FROM stdin;
2	Susan	susan@example.com	pbkdf2:sha256:150000$bZIMiTQc$dd2ca67c9919253be1d273d25c3c0b0cdf1630abb60e70ef8b2cf8395dcf7121	\N	2021-04-13 13:18:24.967932	\N
1	Hezzi	a.hezret@outlook.com	pbkdf2:sha256:150000$lr6BIdoQ$61b198c2f7e331492441de5c8bd21bc14475f769cef4d17b620b96392f7b2fd8	\N	2021-04-13 16:37:17.802992	\N
4	John	john@example.com	pbkdf2:sha256:150000$2PDO8r89$6809e3968e137e729fccadab5abccd5b342f96c3123eaa691e769238b39699cf	\N	2021-04-13 16:49:54.935212	\N
3	Begli	begjan.begli@mail.ru	pbkdf2:sha256:150000$c7tEEpJw$f12713d35c13a9d4f566f3c993b35cf14bd2acfd449d7865c16613c37a75fda7	\N	2021-04-13 10:47:53.986306	\N
\.


--
-- Name: post_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tcadmin
--

SELECT pg_catalog.setval('public.post_id_seq', 7, true);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: tcadmin
--

SELECT pg_catalog.setval('public.user_id_seq', 4, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: tcadmin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: post post_pkey; Type: CONSTRAINT; Schema: public; Owner: tcadmin
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_pkey PRIMARY KEY (id);


--
-- Name: user user_avatar_img_key; Type: CONSTRAINT; Schema: public; Owner: tcadmin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_avatar_img_key UNIQUE (avatar_img);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: tcadmin
--

ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: ix_post_timestamp; Type: INDEX; Schema: public; Owner: tcadmin
--

CREATE INDEX ix_post_timestamp ON public.post USING btree ("timestamp");


--
-- Name: ix_user_email; Type: INDEX; Schema: public; Owner: tcadmin
--

CREATE UNIQUE INDEX ix_user_email ON public."user" USING btree (email);


--
-- Name: ix_user_username; Type: INDEX; Schema: public; Owner: tcadmin
--

CREATE UNIQUE INDEX ix_user_username ON public."user" USING btree (username);


--
-- Name: followers followers_followed_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tcadmin
--

ALTER TABLE ONLY public.followers
    ADD CONSTRAINT followers_followed_id_fkey FOREIGN KEY (followed_id) REFERENCES public."user"(id);


--
-- Name: followers followers_follower_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tcadmin
--

ALTER TABLE ONLY public.followers
    ADD CONSTRAINT followers_follower_id_fkey FOREIGN KEY (follower_id) REFERENCES public."user"(id);


--
-- Name: post post_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: tcadmin
--

ALTER TABLE ONLY public.post
    ADD CONSTRAINT post_user_id_fkey FOREIGN KEY (user_id) REFERENCES public."user"(id);


--
-- PostgreSQL database dump complete
--

