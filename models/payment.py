#!/usr/bin/env python3

# Import
from app import db


class PaymentStatus(db.Model):
    __tablename__ = "payment"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    is_paid = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<PaymentStatus(email='{self.email}', is_paid={self.is_paid})>"