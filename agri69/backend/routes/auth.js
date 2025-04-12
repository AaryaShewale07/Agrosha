import express from "express";
import jwt from "jsonwebtoken";
import multer from "multer";       // 👈 Add multer
import path from "path";           // 👈 For filename extension
import User from "../models/User.js";

const router = express.Router();
const SECRET_KEY = process.env.JWT_SECRET || "yourSecretKey";

// 🔧 Multer config for image uploads
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, "uploads/");
  },
  filename: function (req, file, cb) {
    const ext = path.extname(file.originalname);
    cb(null, Date.now() + ext); // unique filename
  },
});
const upload = multer({ storage: storage });


// ✅ LOGIN route with JWT
router.post("/login", async (req, res) => {
  const { email, password } = req.body;

  try {
    const existingUser = await User.findOne({ email });

    if (!existingUser) {
      return res.status(404).json({ message: "User not found. Please sign up first." });
    }

    if (existingUser.password !== password) {
      return res.status(401).json({ message: "Invalid password" });
    }

    const token = jwt.sign(
      { id: existingUser._id, email: existingUser.email },
      SECRET_KEY,
      { expiresIn: "1h" }
    );

    res.status(200).json({
      message: "✅ Logged in successfully",
      user: existingUser,
      token: token,
    });

  } catch (error) {
    res.status(500).json({ message: "❌ Login failed", error: error.message });
  }
});


// ✅ SIGNUP route with JWT
router.post("/signup", async (req, res) => {
  const { name, email, password } = req.body;

  try {
    const existingUser = await User.findOne({ email });
    if (existingUser) {
      return res.status(400).json({ message: "User already exists" });
    }

    const newUser = new User({ name, email, password });
    await newUser.save();

    const token = jwt.sign(
      { id: newUser._id, email: newUser.email },
      SECRET_KEY,
      { expiresIn: "1h" }
    );

    res.status(201).json({
      message: "✅ User registered successfully",
      user: newUser,
      token: token,
    });

  } catch (error) {
    res.status(500).json({ message: "❌ Registration failed", error: error.message });
  }
});


// ✅ PROFILE UPDATE route with image upload
router.post("/profile", upload.single("profilePic"), async (req, res) => {
  try {
    const { name, email, phone } = req.body;
    const profilePicPath = req.file ? req.file.path : null;

    // ⚠️ Save logic: Adjust according to your DB usage
    // For now: just return the uploaded data
    res.json({
      success: true,
      message: "Profile updated",
      data: {
        name,
        email,
        phone,
        profilePicPath,
      },
    });

  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Profile update failed",
      error: error.message,
    });
  }
});

export default router;
