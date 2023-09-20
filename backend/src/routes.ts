import { Router } from "express";

const dashboardRoutes = Router();

const users = [{
    id: 1,
    name: "Gustav",
    email: "gustavuwe.123@gmail.com",
    password: "ggpranois123"
}]

dashboardRoutes.post("/", (req, res) => {
    const { email, password } = req.body;

    const user = users.find(user => user.email === email && user.password === password)

    if (user) {
        res.status(200).json(user);
    }

    return res.status(401).json({ message: 'Invalid Credentials' })
});

export { dashboardRoutes }